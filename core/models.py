"""
Database Models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save



class UserManager(BaseUserManager):
    """Manager for user models"""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Email cannot be empty")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None):
        """Create a new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

# This signal is fired after a User object has been saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_coin(sender, instance, created, **kwargs):
    if created: # only for newly created User objects
        Coin.objects.create(user=instance)


class Item(models.Model):
    """Item object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    transaction_id = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=5, decimal_places=2)
    # link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Coin(models.Model):
    """Coin object."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    num_coins = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.level = self.get_level()
        super().save(*args, **kwargs)

    def get_level(self):
        if self.num_coins < 1000:
            return 1
        elif self.num_coins < 3000:
            return 2
        elif self.num_coins < 10000:
            return 3
        elif self.num_coins < 25000:
            return 4
        else:
            return 5

    def __str__(self):
        return f'{self.user.email}: Coins-{self.num_coins}, Level-{self.level}'
