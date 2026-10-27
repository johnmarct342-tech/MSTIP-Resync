from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
        ('ADMIN', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"