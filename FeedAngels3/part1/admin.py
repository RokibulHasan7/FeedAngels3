from django.contrib import admin
from .models import CustomUser
from .models import Volunteer
from .models import PickUppoints

admin.site.register(CustomUser)
admin.site.register(Volunteer)
admin.site.register(PickUppoints)
