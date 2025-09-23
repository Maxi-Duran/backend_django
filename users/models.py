from django.db import models
from django.contrib.auth.hashers import check_password
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)