from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('booking/new/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/checkin/', views.check_in, name='check_in'),
    path('booking/<int:booking_id>/checkout/', views.check_out, name='check_out'),
    path('reports/occupancy/', views.occupancy_report, name='occupancy_report'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/revenue/pdf/', views.revenue_report_pdf, name='revenue_report_pdf'),
    path('reports/occupancy/pdf/', views.occupancy_report_pdf, name='occupancy_report_pdf'),
]
