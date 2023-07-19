from django.db import models
import uuid


class Hostel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=100)
    available_rooms = models.IntegerField()
    description = models.TextField(max_length=1000)
    rating = models.FloatField()
