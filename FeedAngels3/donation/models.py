from django.db import models
from django.contrib.auth import get_user_model
from part1.models import CustomUser
User = get_user_model()

class donateMoney(models.Model):
    made_by = models.ForeignKey(CustomUser, related_name='donateMoney', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class donateFood(models.Model):
    made_by = models.ForeignKey(CustomUser, related_name='donateFood', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    expiration_date = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    is_approved = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.made_by
