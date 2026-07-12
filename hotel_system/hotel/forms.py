from typing import cast

from django import forms
from django.forms import ModelChoiceField

from .models import Booking, RoomStatus


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest', 'room', 'staff', 'check_in_date', 'check_out_date']
        widgets = {
            'guest': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'staff': forms.Select(attrs={'class': 'form-select'}),
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restricting the queryset to available rooms also makes Django reject,
        # at validation time, a room that was booked by someone else between
        # page load and submit - closing the race window a plain FK save would miss.
        room_field = cast(ModelChoiceField, self.fields['room'])
        assert room_field.queryset is not None, 'ModelForm did not build a room queryset'
        room_field.queryset = room_field.queryset.filter(status=RoomStatus.AVAILABLE)
        room_field.error_messages['invalid_choice'] = 'That room is no longer available.'

    def clean(self):
        cleaned_data = super().clean() or {}
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if not check_in_date or not check_out_date:
            return cleaned_data

        if check_out_date <= check_in_date:
            self.add_error('check_out_date', 'Check-out date must be after the check-in date.')

        return cleaned_data
