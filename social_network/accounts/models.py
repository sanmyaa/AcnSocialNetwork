from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from simple_history.models import HistoricalRecords

from social_network.utils.modelutils import TimeStampable


class UserManager(BaseUserManager):
    """
    Custom manager for User model with email as the unique identifier.
    """

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by converting it to lowercase.
        """
        return email.lower()

    def _create_user(self, *, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The email field must be set")
        if not password:
            raise ValueError("The password field must be set")

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, *, email, password, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, *, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, password=password, **extra_fields)

    def create(self, **kwargs):
        """
        Create and save a user using overridden methods.
        """
        return self.create_user(**kwargs)


class User(AbstractUser, TimeStampable):
    """
    Custom user model where email is the unique identifier.
    """

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    history = HistoricalRecords(inherit=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ("-id",)
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

    def __str__(self):
        """
        Return a string representation of the user.
        """
        return f"{self.name} ({self.email})"
