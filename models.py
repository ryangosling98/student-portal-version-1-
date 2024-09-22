from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=100)
    gpa = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"