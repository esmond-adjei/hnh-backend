from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid


class Hostel(models.Model):
    manager = models.ForeignKey(
        'usermanagement.HManager',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hostels_managed'
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=100)
    available_rooms = models.IntegerField(default=0)
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=2.50, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True)

    @property
    def available_rooms(self):
        return self.room_set.aggregate(total_available=models.Sum('number_available'))['total_available']

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    BEDSPACE_CHOICES = (
        ('4-in-1', '4 persons in 1 room'),
        ('3-in-1', '3 persons in 1 room'),
        ('2-in-1', '2 persons in 1 room'),
        ('1-in-1', '1 person in 1 room'),
    )

    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    # there might be conflict here in the future. we'll come back
    room_id = models.CharField(max_length=10, unique=True, primary_key=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    bedspace = models.CharField(max_length=10, choices=BEDSPACE_CHOICES)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    number_available = models.IntegerField(default=1)
    amenities = models.ManyToManyField(Amenity, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"Room {self.room_id} in {self.hostel.name}"
