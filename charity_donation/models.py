from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Institution(models.Model):
    FOUNDATION = 0
    NON_GOVERMENTAL_ORGANIZATION = 1
    LOCAL_COLLECTION = 2

    TYPES_OF_INSTITUTION = (
        (FOUNDATION, "foundation"),
        (NON_GOVERMENTAL_ORGANIZATION, "non-governmental organization"),
        (LOCAL_COLLECTION, "local collection"),
    )

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.IntegerField(choices=TYPES_OF_INSTITUTION, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.quantity
