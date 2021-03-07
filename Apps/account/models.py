from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from BeakHub import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):

        if not username:
            raise ValueError('The username is mandatory')
        if email:
            email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, None, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True, db_index=True, max_length=100,
        verbose_name='Username'
    )
    email = models.EmailField(
        blank=True, null=True, unique=True, db_index=True,
        verbose_name='Email'
    )
    first_name = models.CharField(
        null=True, blank=True, max_length=200,
        verbose_name='First name'
    )
    last_name = models.CharField(
        null=True, blank=True, max_length=200,
        verbose_name='Last name'
    )
    birth_date = models.DateField(
        blank= True, null=True,
        verbose_name='Birth Date'
    )
    phone = PhoneNumberField(
        blank=True, null=True,
        verbose_name='Phone Number'
    )
    country = CountryField(
        default=settings.DEFAULT_COUNTRY,
        verbose_name='Countries'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff ?'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is Activated ?'
    )
    activation_key = models.UUIDField(
        unique=True, default=uuid4, editable=False,
        verbose_name='Activation Key'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Date of inscription'
    )
    date_update = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Updated'
    )
    user_condition_is_read = models.BooleanField(
        default=False,
        verbose_name='User conditions is read ?'
    )
    profile_picture = models.ImageField(
        upload_to="photo_user/", null=True, blank=True,
        verbose_name='Profile Picture'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = 'account'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        if self.email:
            return self.email
        return self.username
