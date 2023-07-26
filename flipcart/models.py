from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class UserManager(BaseUserManager):
    def create_user( username, email, password, dob=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = User.normalize_email(email)
        user = User.model(username=username, email=email, date_of_birth=dob)
        user.set_password(password)
        user.save(using=user)
        return user

    def create_superuser(self, username, email, password=None, date_of_birth=None):
        user = user.create_user(username, email, password, date_of_birth)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254)
    dob = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username
