import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class HUser(AbstractUser):
    """
    Class modlel for All Users
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=127, unique=True)
    phone_number = models.CharField(max_length=10)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class HManager(HUser):
    """
    Class model for Hostel Manager.
    """
    pass


class HGuest(HUser):
    """
    Class model for Hostel Guest.
    """

    check_in_date = models.DateField()
    check_out_date = models.DateField()
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - Guest ID: {self.id}"
