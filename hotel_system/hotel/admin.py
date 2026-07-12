from django.contrib import admin
from .models import RoomType, Room, Guest, Staff, Booking

# Register your models here.
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ('guest', 'check_in_date', 'check_out_date', 'status')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'floor', 'status')
    list_filter = ('status', 'room_type')
    inlines = [BookingInline]


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_id', 'last_name', 'first_name', 'contact_number')
    search_fields = ('last_name', 'first_name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'guest', 'room', 'check_in_date', 'check_out_date', 'status')
    list_filter = ('status',)


admin.site.register(RoomType)
admin.site.register(Staff)
