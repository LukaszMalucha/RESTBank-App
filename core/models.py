import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# Manager Class
class UserManager(BaseUserManager):

    # extra fields in case we want to extend class in a future
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # helper function to lowercase email
        user.set_password(password)  # hash helper function
        user.save(using=self._db)  # in case of multiple dbs
        return user

    # create superuser helper function
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_vip = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Model Class
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that allows using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_vip = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Assign user manager to objects attribute
    objects = UserManager()

    USERNAME_FIELD = 'email'  # customize to email

    ### Add  AUTH_USER_MODEL to settings !!!





class Instrument(models.Model):
    """Financial instrument for customer portfolio"""
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.symbol


class Portfolio(models.Model):
    """Customer's account details"""
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assets = models.ManyToManyField('Asset')

    def __str__(self):
        return f"{self.owner}-{self.title}"


class Asset(models.Model):
    """Customer owned asset"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.instrument}"



class Transaction(models.Model):
    account = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=5)  ## buy or sell

    def __str__(self):
        return f"{self.account}-{self.instrument}-{self.created_at}"
