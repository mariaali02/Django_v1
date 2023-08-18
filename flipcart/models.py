from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    DateOfBirth = models.DateField( null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        region="PK",  # Set the default region to Pakistan
    )
    def __str__(self):
        return f"UserProfile for {self.user.username}"