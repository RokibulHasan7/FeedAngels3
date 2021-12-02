from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False)
    mobileNum = models.PositiveIntegerField(null=False, blank=False)


class Volunteer(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, )
    address = models.CharField(max_length=200)
    img = models.ImageField(upload_to="media")

    def __str__(self):
        return '%s' % self.username


class PickUppoints(models.Model):
    Division = models.CharField(max_length=200)
    District = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    img = models.ImageField(upload_to="media")
