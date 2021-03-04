from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from BeakHub import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):

        if not username:
            raise ValueError(_('The username is mandatory'))
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
        verbose_name=_('Username')
    )
    email = models.EmailField(
        blank=True, null=True, unique=True, db_index=True,
        verbose_name=_('Email')
    )
    first_name = models.CharField(
        null=True, blank=True, max_length=200,
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        null=True, blank=True, max_length=200,
        verbose_name=_('Last name')
    )
    birth_date = models.DateField(
        blank= True, null=True,
        verbose_name=_('Birth Date')
    )
    phone = PhoneNumberField(
        blank=True, null=True,
        verbose_name=_('Phone Number')
    )
    country = CountryField(
        default=settings.DEFAULT_COUNTRY,
        verbose_name=_('Countries')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Is Staff ?')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Is Activated ?')
    )
    activation_key = models.UUIDField(
        unique=True, default=uuid4, editable=False,
        verbose_name=_('Activation Key')
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name=_('Date of inscription')
    )
    date_update = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date Updated')
    )
    user_condition_is_read = models.BooleanField(
        default=False,
        verbose_name=_('User conditions is read ?')
    )
    profile_picture = models.ImageField(
        upload_to="photo_user/", null=True,
        verbose_name=_('Profile Picture')
    )

    objects = UserManager()

    class Meta:
        app_label = _('Account')
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        if self.email:
            return self.email
        return self.username
