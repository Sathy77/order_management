from django.db import models
from django.contrib.auth.models import User  # Or your custom user model
from django.utils import timezone
from datetime import timedelta
import datetime

class Otp(models.Model):
    phone = models.CharField(max_length=14)  # Reference to the user
    otp_code = models.CharField(max_length=4)  # OTP code, assuming 4 digits
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        # Check if OTP is expired (4 minutes)
        expiration_time = self.created_at + datetime.timedelta(minutes=4)
        return timezone.now() > expiration_time
    
    def __str__(self):
        return f"OTP for {self.phone} - {self.otp_code}"