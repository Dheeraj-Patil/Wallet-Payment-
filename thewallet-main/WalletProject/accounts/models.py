from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_wuser(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_wallet_user', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ custom user model that supports using emails instead user names"""
    username = None
    email = models.EmailField(max_length=255, unique=True)
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,12}$',
        message="Phone number must be entered in the format: '+918080809804'. Up to 12 digits allowed.")
    wallet_phone = models.CharField(
        validators=[mobile_regex], max_length=15, blank=True)
    is_wallet_user = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Wallet(models.Model):
    """Model to Store Wallet Meta

    Args:
        models ([type]): [description]
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=15)
    second_email = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_email', limit_choices_to={
            'is_wallet_user': False})
    balance = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return 'wallet ' + str(self.user)


class BankAccount(models.Model):
    """Model to Store Wallet User Profile

    Args:
        models ([type]): [description]
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    bank_id = models.CharField(max_length=15)
    account_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.wallet)
