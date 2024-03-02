# Django imports 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from sts.managers import UserManager
from django.contrib.gis.db.models import PointField

# Local modules imports



class Captain(models.Model):

    name = models.CharField(max_length=32, blank=True, null=True),
    email = models.EmailField()
    phone_number = models.CharField(blank=True, null=True)
    is_available = models.BooleanField(default = True)
    def __str__(self):
        return self.email
    
class User(AbstractBaseUser, PermissionsMixin):

    class UserType(models.TextChoices):
        CAPTAIN = ("CAPTAIN", "Captian")
        CLIENT = ("CLIENT", "Client")
        ADMIN = ("ADMIN", "Admin")
    
    base_type = UserType.CLIENT
    user_type = models.CharField(max_length = 16, choices = UserType.choices, default = base_type )
    name = models.CharField(max_length = 256, unique = False, db_index = True)
    email = models.EmailField(_("email address"), unique=True, db_index = True)
    location = PointField(srid=4326, null=True, blank=True)
    otp = models.CharField(max_length = 200, null = True, blank = True)
    phone_number = models.CharField(max_length = 30)
    is_verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        
    def __str__(self):
        return self.email


class Trip(models.Model):
    class Status(models.TextChoices):
        PENDING = ("PENDING", "Pending")
        ACCEPTED = ("ACCEPTED", "Accepted")
        REJECTED = ("REJECTED", "Rejected")
    
    start = PointField(srid=4326, blank=True, null=True,)
    end = PointField(srid=4326, blank=True, null=True)
    price = models.CharField(max_length = 256)
    distance = models.CharField(max_length = 256)
    client_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    captain_ID = models.ForeignKey(Captain, on_delete=models.CASCADE)
    trip_status = models.CharField(max_length = 32,choices = Status.choices, blank=True, null=True)


# class AcceptedTrips(mod)