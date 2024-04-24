from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class FileModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    name = models.CharField(max_length=64)
    content = models.CharField(max_length=10000)
    date_time = models.DateTimeField(default=now)