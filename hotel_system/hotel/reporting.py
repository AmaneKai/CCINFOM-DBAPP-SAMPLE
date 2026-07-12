"""Pure report-building functions shared by the HTML and PDF report views."""
import calendar

from .models import Booking, Room


def percent_change(current_value, previous_value):
    if not previous_value:
        return None
    return round(((current_value - previous_value) / previous_value) * 100, 1)


def _attach_change_from_previous_month(monthly_data, value_key, change_key, as_percent=False):
    for index, row in enumerate(monthly_data):
        if index == 0:
            row[change_key] = None
            continue

        previous_value = monthly_data[index - 1][value_key]
        if as_percent:
            row[change_key] = percent_change(row[value_key], previous_value)
        else:
            row[change_key] = round(row[value_key] - previous_value, 1)

    return monthly_data


def monthly_booking_counts(year):
    return [
        Booking.objects.filter(check_in_date__year=year, check_in_date__month=month_number).count()
        for month_number in range(1, 13)
    ]


def monthly_revenue_totals(year):
    totals = []
    for month_number in range(1, 13):
        bookings_this_month = Booking.objects.filter(
            check_in_date__year=year, check_in_date__month=month_number
        ).select_related('room__room_type')
        revenue = sum((booking.total_cost for booking in bookings_this_month), 0)
        totals.append((revenue, bookings_this_month.count()))
    return totals


def build_occupancy_report(year):
    total_rooms = Room.objects.count() or 1

    monthly_data = [
        {
            'month': calendar.month_abbr[month_number],
            'bookings': booking_count,
            'rate': round((booking_count / total_rooms) * 100, 1),
        }
        for month_number, booking_count in enumerate(monthly_booking_counts(year), start=1)
    ]
    _attach_change_from_previous_month(monthly_data, value_key='rate', change_key='mom_change')

    peak_month_row = max(monthly_data, key=lambda row: row['rate'])

    return {
        'monthly_data': monthly_data,
        'total_rooms': total_rooms,
        'avg_occupancy': round(sum(row['rate'] for row in monthly_data) / 12, 1),
        'peak_month': peak_month_row['month'],
        'peak_rate': peak_month_row['rate'],
        'total_bookings_year': sum(row['bookings'] for row in monthly_data),
    }


def build_revenue_report(year):
    monthly_totals = enumerate(monthly_revenue_totals(year), start=1)
    monthly_data = [
        {'month': calendar.month_abbr[month_number], 'revenue': revenue, 'bookings': booking_count}
        for month_number, (revenue, booking_count) in monthly_totals
    ]
    _attach_change_from_previous_month(
        monthly_data, value_key='revenue', change_key='mom_growth', as_percent=True
    )

    total_revenue = sum(row['revenue'] for row in monthly_data)
    prior_year_revenue = sum(revenue for revenue, _ in monthly_revenue_totals(year - 1))

    return {
        'monthly_data': monthly_data,
        'total_revenue': total_revenue,
        'total_bookings': sum(row['bookings'] for row in monthly_data),
        'avg_monthly': total_revenue / 12,
        'yoy_growth': percent_change(total_revenue, prior_year_revenue),
    }
