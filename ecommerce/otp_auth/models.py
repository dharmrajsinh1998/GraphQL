from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    otp = models.CharField(max_length=6)
    resend_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.email)
