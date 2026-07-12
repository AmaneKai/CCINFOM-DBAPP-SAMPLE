from datetime import date
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from .forms import BookingForm
from .models import Booking, BookingStatus, Guest, Room, RoomStatus, RoomType, Staff
from .reporting import build_occupancy_report, build_revenue_report, percent_change


def create_room_type(type_code='STD', base_rate='1000.00'):
    return RoomType.objects.create(
        type_code=type_code, type_name='Standard', base_rate=Decimal(base_rate)
    )


def create_room(room_type, room_number='101', status=RoomStatus.AVAILABLE):
    return Room.objects.create(room_number=room_number, room_type=room_type, floor=1, status=status)


def create_guest():
    return Guest.objects.create(last_name='Cruz', first_name='Ana', contact_number='0900000000')


def create_booking(room, guest, check_in_date, check_out_date, status=BookingStatus.RESERVED):
    return Booking.objects.create(
        guest=guest, room=room, check_in_date=check_in_date,
        check_out_date=check_out_date, status=status,
    )


class BookingDomainLogicTests(TestCase):
    def setUp(self):
        self.room_type = create_room_type(base_rate='1500.00')
        self.room = create_room(self.room_type)
        self.guest = create_guest()

    def test_nights_counts_full_days_between_check_in_and_check_out(self):
        booking = create_booking(self.room, self.guest, date(2026, 1, 1), date(2026, 1, 4))

        self.assertEqual(booking.nights, 3)

    def test_total_cost_multiplies_nights_by_room_type_base_rate(self):
        booking = create_booking(self.room, self.guest, date(2026, 1, 1), date(2026, 1, 4))

        self.assertEqual(booking.total_cost, Decimal('4500.00'))

    def test_total_cost_is_zero_for_a_same_day_stay(self):
        booking = create_booking(self.room, self.guest, date(2026, 1, 1), date(2026, 1, 1))

        self.assertEqual(booking.total_cost, Decimal('0.00'))


class PercentChangeTests(TestCase):
    def test_returns_none_when_previous_value_is_zero(self):
        self.assertIsNone(percent_change(current_value=100, previous_value=0))

    def test_returns_none_when_previous_value_is_none(self):
        self.assertIsNone(percent_change(current_value=100, previous_value=None))

    def test_computes_rounded_percentage_change(self):
        self.assertEqual(percent_change(current_value=150, previous_value=100), 50.0)

    def test_computes_negative_percentage_change(self):
        self.assertEqual(percent_change(current_value=50, previous_value=100), -50.0)


class BuildRevenueReportTests(TestCase):
    def setUp(self):
        self.room_type = create_room_type(base_rate='1000.00')
        self.room = create_room(self.room_type)
        self.guest = create_guest()

    def test_month_with_no_bookings_has_zero_revenue(self):
        report = build_revenue_report(2026)

        january_row = report['monthly_data'][0]
        self.assertEqual(january_row['revenue'], 0)
        self.assertEqual(january_row['bookings'], 0)

    def test_total_revenue_sums_every_booking_in_the_year(self):
        create_booking(self.room, self.guest, date(2026, 1, 1), date(2026, 1, 3))
        create_booking(self.room, self.guest, date(2026, 2, 1), date(2026, 2, 2))

        report = build_revenue_report(2026)

        self.assertEqual(report['total_revenue'], Decimal('3000.00'))
        self.assertEqual(report['total_bookings'], 2)

    def test_month_over_month_growth_is_none_for_january(self):
        report = build_revenue_report(2026)

        self.assertIsNone(report['monthly_data'][0]['mom_growth'])

    def test_yoy_growth_is_none_when_there_is_no_prior_year_data(self):
        create_booking(self.room, self.guest, date(2026, 1, 1), date(2026, 1, 3))

        report = build_revenue_report(2026)

        self.assertIsNone(report['yoy_growth'])


class BuildOccupancyReportTests(TestCase):
    def setUp(self):
        self.room_type = create_room_type()
        self.guest = create_guest()

    def test_occupancy_rate_uses_total_room_count_as_the_denominator(self):
        create_room(self.room_type, room_number='101')
        create_room(self.room_type, room_number='102')
        create_booking(
            Room.objects.get(room_number='101'), self.guest, date(2026, 3, 1), date(2026, 3, 2)
        )

        report = build_occupancy_report(2026)

        march_row = report['monthly_data'][2]
        self.assertEqual(march_row['rate'], 50.0)

    def test_does_not_divide_by_zero_when_there_are_no_rooms(self):
        report = build_occupancy_report(2026)

        self.assertEqual(report['avg_occupancy'], 0.0)


class BookingFormTests(TestCase):
    def setUp(self):
        self.room_type = create_room_type()
        self.available_room = create_room(self.room_type, room_number='101')
        self.occupied_room = create_room(
            self.room_type, room_number='102', status=RoomStatus.OCCUPIED
        )
        self.guest = create_guest()
        self.staff = Staff.objects.create(last_name='Reyes', first_name='Jon', position='Clerk')

    def _form_data(self, **overrides):
        data = {
            'guest': self.guest.guest_id,
            'room': self.available_room.room_number,
            'staff': self.staff.staff_id,
            'check_in_date': '2026-08-01',
            'check_out_date': '2026-08-03',
        }
        data.update(overrides)
        return data

    def test_valid_data_is_accepted(self):
        form = BookingForm(data=self._form_data())

        self.assertTrue(form.is_valid())

    def test_rejects_check_out_on_or_before_check_in(self):
        form = BookingForm(data=self._form_data(check_out_date='2026-08-01'))

        self.assertFalse(form.is_valid())
        self.assertIn('check_out_date', form.errors)

    def test_rejects_a_room_that_is_not_available(self):
        form = BookingForm(data=self._form_data(room=self.occupied_room.room_number))

        self.assertFalse(form.is_valid())
        self.assertIn('room', form.errors)


class ReportPageRenderingTests(TestCase):
    """Guards the JSON/chart serialization boundary, not just the pure report math."""

    def setUp(self):
        self.client = Client()
        room_type = create_room_type(base_rate='1000.00')
        room = create_room(room_type)
        guest = create_guest()
        create_booking(room, guest, date(2026, 1, 1), date(2026, 1, 3))

    def test_revenue_report_page_renders_with_bookings_present(self):
        response = self.client.get(reverse('revenue_report'), {'year': '2026'})

        self.assertEqual(response.status_code, 200)

    def test_revenue_report_pdf_renders_with_bookings_present(self):
        response = self.client.get(reverse('revenue_report_pdf'), {'year': '2026'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_occupancy_report_page_renders_with_bookings_present(self):
        response = self.client.get(reverse('occupancy_report'), {'year': '2026'})

        self.assertEqual(response.status_code, 200)

    def test_occupancy_report_pdf_renders_with_bookings_present(self):
        response = self.client.get(reverse('occupancy_report_pdf'), {'year': '2026'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_report_pages_fall_back_to_the_current_year_on_a_malformed_year_param(self):
        response = self.client.get(reverse('revenue_report'), {'year': 'not-a-year'})

        self.assertEqual(response.status_code, 200)
