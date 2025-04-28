from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Role.SYSTEM_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        SYSTEM_ADMIN = 'SYSTEM_ADMIN', _('System Admin')
        USER = 'USER', _('User')
    
    # Remove username from required fields
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        blank=True,
        null=True
    )
    
    email = models.EmailField(_('email address'), unique=True, max_length=250)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'username']

    objects = UserManager()  # Assign custom manager

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{uuid.uuid4().hex[:10]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_system_admin(self):
        return self.role == self.Role.SYSTEM_ADMIN
    
    @property
    def is_user(self):
        return self.role == self.Role.USER

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'