from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False)
    mobileNum = models.PositiveIntegerField(null=True, blank=True)


class Volunteer(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, )
    address = models.CharField(max_length=200)
    img = models.ImageField(upload_to=filepath, null=True, blank=True)

    def __str__(self):
        return '%s' % self.username


class PickUppoints(models.Model):
    Division = models.CharField(max_length=200)
    District = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    img = models.ImageField(upload_to=filepath)


