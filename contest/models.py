import uuid
from django.db import models
from users.models import CustomUser
# Create your models here.
class Participant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)
    participation_code = models.UUIDField(default=uuid.uuid4, editable=False)
    won_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.participation_code}"