from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    email = models.EmailField(null=True,max_length=254)
    date_of_birth = models.DateField( null=True, blank=True)
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
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='deleted_users', null=True ,blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Other methods and fields ...

    def soft_delete(self, deleted_by):
        self.deleted = True
        self.deleted_by = deleted_by
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted = False
        self.deleted_by = None
        self.deleted_at = None
        self.save()
    def __str__(self):
        return f"UserProfile for {self.user.username}"
    


