import uuid
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = (
        ('LECTURE', 'Lecture Room'),
        ('LAB', 'Computer Laboratory'),
        ('AVR', 'Audio Visual Room'),
    )
    room_name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.room_name} ({self.get_room_type_display()})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled by User'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reference_no = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.room_name} - {self.date} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.reference_no:
            # Generate a random 8-character hex string (e.g., 'A1B2C3D4')
            self.reference_no = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

class ClassSchedule(models.Model):
    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    )
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100) # e.g., "IT 101"
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject_name} - {self.room.room_name} ({self.get_day_of_week_display()})"    