from django.contrib import admin
from .models import Room, Booking, ClassSchedule

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(ClassSchedule)