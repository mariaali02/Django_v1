from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, date_of_birth=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, date_of_birth=None):
        user = self.create_user(username, email, password, date_of_birth)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username
