from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class StudentUser(AbstractUser):
    phone_number = models.CharField(default='', max_length=12)
    dia_chi = models.CharField(default='', max_length=255)