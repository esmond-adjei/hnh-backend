import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
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
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name, verbose_name_plural = "Manager", "Managers"


class HGuest(HUser):
    """
    Class model for Hostel Guest.
    """

    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)
    emergency_contact_name = models.CharField(
        blank=True, null=True, max_length=255)
    emergency_contact_phone = models.CharField(
        blank=True, null=True, max_length=20)
    special_requests = models.TextField(blank=True, null=True)
    collections = models.ManyToManyField('Collection', related_name='users')

    def __str__(self):
        return f"{self.full_name} - Guest ID: {self.id}"

    class Meta:
        verbose_name, verbose_name_plural = "Guest", "Guests"



class Collection(models.Model):
    """
    Class model for Collection.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=125)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='collections')
    rooms = models.ManyToManyField('hostel.Room', related_name='collections')

    def __str__(self):
        return f"Collection {self.id} for {self.user}"
