import json
from datetime import date

from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking, BookingStatus, Room, RoomStatus
from .pdf_rendering import render_to_pdf
from .report_charts import make_line_chart
from .reporting import build_occupancy_report, build_revenue_report

REVENUE_CHART_COLOR = '#2563eb'
OCCUPANCY_CHART_COLOR = '#0891b2'


def _requested_year(request):
    year_param = request.GET.get('year')
    if not year_param or not year_param.isdigit():
        return date.today().year
    return int(year_param)


def _available_report_years():
    current_year = date.today().year
    return [current_year - 1, current_year]


def _chart_color_context(hex_color, fill_opacity=0.1):
    red, green, blue = (int(hex_color.lstrip('#')[index:index + 2], 16) for index in (0, 2, 4))
    return {
        'chart_border_color': hex_color,
        'chart_fill_color': f'rgba({red}, {green}, {blue}, {fill_opacity})',
    }


def dashboard(request):
    recent_bookings = (
        Booking.objects.select_related('guest', 'room').order_by('-check_in_date')[:20]
    )

    total_rooms = Room.objects.count()
    occupied_room_count = Room.objects.filter(status=RoomStatus.OCCUPIED).count()
    occupancy_rate = round((occupied_room_count / total_rooms) * 100, 1) if total_rooms else 0

    today = date.today()
    bookings_this_month = Booking.objects.filter(
        check_in_date__year=today.year, check_in_date__month=today.month
    ).select_related('room__room_type')
    booking_count_this_month = bookings_this_month.count()

    average_stay_nights = 0
    if booking_count_this_month:
        total_nights = sum(booking.nights for booking in bookings_this_month)
        average_stay_nights = round(total_nights / booking_count_this_month, 1)

    return render(request, 'dashboard.html', {
        'bookings': recent_bookings,
        'occupancy_rate': occupancy_rate,
        'occupied_now': occupied_room_count,
        'total_rooms': total_rooms,
        'available_rooms': total_rooms - occupied_room_count,
        'mtd_revenue': sum((booking.total_cost for booking in bookings_this_month), 0),
        'mtd_bookings': booking_count_this_month,
        'avg_stay': average_stay_nights,
    })


def create_booking(request):
    if request.method != 'POST':
        return render(request, 'create_booking.html', {'form': BookingForm()})

    form = BookingForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_booking.html', {'form': form})

    booking = form.save(commit=False)
    booking.status = BookingStatus.RESERVED
    booking.save()

    booking.room.status = RoomStatus.RESERVED
    booking.room.save()
    return redirect('dashboard')


def check_in(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method != 'POST':
        return render(request, 'check_in.html', {'booking': booking})

    booking.status = BookingStatus.CHECKED_IN
    booking.save()
    booking.room.status = RoomStatus.OCCUPIED
    booking.room.save()
    return redirect('dashboard')


def check_out(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method != 'POST':
        return render(request, 'check_out.html', {
            'booking': booking,
            'nights': booking.nights,
            'total': booking.total_cost,
        })

    booking.status = BookingStatus.COMPLETED
    booking.save()
    booking.room.status = RoomStatus.AVAILABLE
    booking.room.save()
    return redirect('dashboard')


def occupancy_report(request):
    year = _requested_year(request)
    report = build_occupancy_report(year)

    return render(request, 'occupancy_report.html', {
        'year': year,
        'available_years': _available_report_years(),
        **report,
        **_chart_color_context(OCCUPANCY_CHART_COLOR),
        'chart_labels': json.dumps([row['month'] for row in report['monthly_data']]),
        'chart_data': json.dumps([row['rate'] for row in report['monthly_data']]),
    })


def revenue_report(request):
    year = _requested_year(request)
    report = build_revenue_report(year)

    return render(request, 'revenue_report.html', {
        'year': year,
        'available_years': _available_report_years(),
        **report,
        **_chart_color_context(REVENUE_CHART_COLOR),
        'chart_labels': json.dumps([row['month'] for row in report['monthly_data']]),
        'chart_data': json.dumps([float(row['revenue']) for row in report['monthly_data']]),
    })


def revenue_report_pdf(request):
    year = _requested_year(request)
    report = build_revenue_report(year)
    monthly_data = report['monthly_data']

    chart_image = make_line_chart(
        [row['month'] for row in monthly_data],
        [float(row['revenue']) for row in monthly_data],
        'Revenue (PHP)', color=REVENUE_CHART_COLOR,
    )

    response = render_to_pdf('pdf/revenue_pdf.html', {
        'year': year,
        'monthly_data': monthly_data,
        'total_revenue': report['total_revenue'],
        'avg_monthly': report['avg_monthly'],
        'best_month': max(monthly_data, key=lambda row: row['revenue']),
        'chart_img': chart_image,
        'generated_on': date.today().strftime('%B %d, %Y'),
    })
    response['Content-Disposition'] = f'attachment; filename="revenue_report_{year}.pdf"'
    return response


def occupancy_report_pdf(request):
    year = _requested_year(request)
    report = build_occupancy_report(year)
    monthly_data = report['monthly_data']

    chart_image = make_line_chart(
        [row['month'] for row in monthly_data],
        [row['rate'] for row in monthly_data],
        'Occupancy (%)', color=OCCUPANCY_CHART_COLOR,
    )

    response = render_to_pdf('pdf/occupancy_pdf.html', {
        'year': year,
        'monthly_data': monthly_data,
        'avg_occupancy': report['avg_occupancy'],
        'peak_month': report['peak_month'],
        'peak_rate': report['peak_rate'],
        'total_rooms': report['total_rooms'],
        'chart_img': chart_image,
        'generated_on': date.today().strftime('%B %d, %Y'),
    })
    response['Content-Disposition'] = f'attachment; filename="occupancy_report_{year}.pdf"'
    return response
