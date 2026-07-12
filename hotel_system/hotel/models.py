from django.db import models


class RoomStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    OCCUPIED = 'occupied', 'Occupied'
    RESERVED = 'reserved', 'Reserved'


class BookingStatus(models.TextChoices):
    RESERVED = 'reserved', 'Reserved'
    CHECKED_IN = 'checked-in', 'Checked in'
    COMPLETED = 'completed', 'Completed'


class RoomType(models.Model):
    type_code = models.CharField(max_length=10, primary_key=True)
    type_name = models.CharField(max_length=50)
    base_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.type_name


class Room(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    floor = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE
    )

    def __str__(self):
        return self.room_number


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=BookingStatus.choices, default=BookingStatus.RESERVED
    )

    def __str__(self):
        return f'Booking #{self.booking_id} - {self.guest}'

    @property
    def nights(self):
        return (self.check_out_date - self.check_in_date).days

    @property
    def total_cost(self):
        return self.nights * self.room.room_type.base_rate
