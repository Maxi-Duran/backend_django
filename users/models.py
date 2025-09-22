from django.db import models
import uuid
# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True)
    def __str__(self):
        return self.email