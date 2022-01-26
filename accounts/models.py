"""
  The reason we have to extend the user model is because:
  1. We need to use email for athentication.
  2. we need first name and second name.
  3. Very !IMPORTANT, we need boolean fields to filter out different users with
  different profiles.

  Of course this comes with a `price`.
"""


import uuid
from django.contrib import messages
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    UnicodeUsernameValidator,
    PermissionsMixin,
)
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.db.models import Q, lookups
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import (
    post_save,
)
from accounts.validators import validate_lastname_length, validate_firstname_length

from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.utils.html import format_html
from ckeditor.fields import RichTextField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("admin", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("active", True)
        extra_fields.setdefault("non", False)
        if extra_fields.get("admin") is not True:
            raise ValueError("Superuser must have admin=True.")

        return self._create_user(email, password, **extra_fields)

    def staff_user(self):
        return self.get_queryset().filter(staff=True)

    def employee_user(self):
        return self.get_queryset().filter(employee=True)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="First name",
        validators=[validate_firstname_length],
        blank=True,
        null=True,
    )
    second_name = models.CharField(
        max_length=100,
        verbose_name="Second name",
        validators=[validate_lastname_length],
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=250, unique=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    buyer = models.BooleanField(default=False)
    employee = models.BooleanField(default=False)
    non = models.BooleanField(default=True) 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "second_name"]
    objects = UserManager()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Takes parameters subject, message, from_email
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def colored_first_name(self):
        return format_html(
            '<a href="#" style="color:{};">{}</a>', "royalblue", self.first_name
        )

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.second_name}"

    @property
    def get_innitials(self):
        def __innitial(param):
            name_list = param.split()
            new = ""
            for name in range(len(name_list)):
                param = name_list[name]
                new += param[0].upper() + "."
            return new

        return __innitial(f"{self.first_name} {self.second_name}")

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_buyer(self):
        return self.buyer

    @property
    def is_employee(self):
        return self.employee

    @property
    def is_non(self):
        return self.non

class GenderChoice(models.TextChoices):
    SELECT = "s", "Select"
    MALE = "m", "Male"
    FEMALE = "f", "Female"


class EmployeeProfile(models.Model):
    GENDER = GenderChoice.choices
    user = models.OneToOneField(
        User, related_name="employee_profile", on_delete=models.CASCADE
    )

    avatar = models.ImageField(
        upload_to="media/profiles/employees/avatars/", null=True, blank=True
    )
    gender = models.CharField(
        choices=GenderChoice.choices, max_length=1, default=GenderChoice.SELECT
    )
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Include your city or your area.",
    )
    resume = models.FileField(
        upload_to="media/profiles/employees/resumes",
        null=True,
        blank=True,
        help_text="Attach your resume most prefferably in word formart.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    @property
    def get_avatar(self):
        return (
            self.avatar.url
        )  # if self.avatar else static('assets/img/team/default-profile-picture.png')


class StaffProfile(models.Model):
    GENDER = GenderChoice.choices
    user = models.OneToOneField(
        User, related_name="staff_profile", on_delete=models.CASCADE
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="First name",
        blank=True,
        null=True,
    )
    second_name = models.CharField(
        max_length=100,
        verbose_name="Second name",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="media/profiles/staff/avatars/", null=True, blank=True
    )
    gender = models.CharField(
        choices=GenderChoice.choices, max_length=1, default=GenderChoice.SELECT
    )
    phone = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Business number for communication",
    )
    resume = RichTextField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="Use 1000 words only. To be pulished in the website.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    @property
    def get_avatar(self):
        return (
            self.avatar.url
        )  # if self.avatar else static('assets/img/team/default-profile-picture.png')


class InnovestUsersMessages(models.Model):
    session_user = models.CharField(null=True, blank=True, max_length=100)
    names = models.CharField(
        max_length=100,
        verbose_name="client name",
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=225)
    # phone = models.CharField(max_length=32, null=True, blank=True, help_text="Optional but more convenient")
    message = models.CharField(
        max_length=1000, default="Innovest Message", null=True, blank=True
    )
    inform_us = models.CharField(
        max_length=1000, help_text="Ask question, Inform us on anything."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SubscriberManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True)


class InnovestSubcribers(models.Model):
    email = models.EmailField(
        max_length=100,
        verbose_name="Subscriber email",
        help_text="We will be sending you new jobs",
    )
    subscribe = models.CharField(
        max_length=1000, default="Innovest subscriber", null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SubscriberManager()

    def __str__(self):
        return self.email


class AccentChoices(models.TextChoices):
    GREEN = "g", "Green"
    RED = "r", "Red"
    BLUE = "b", "Blue"


class Theme(models.Model):
    ACCENT = AccentChoices.choices
    session = models.CharField(
        _("current sesion"), max_length=50, default="", blank=True, null=True)
    light = models.BooleanField(default=True)
    accent = models.CharField(
        choices=AccentChoices.choices, max_length=1, default=AccentChoices.GREEN)

    def __str__(self):
        return self.session
