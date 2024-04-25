from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class FileModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    content = models.BinaryField()
    date_time = models.DateTimeField(default=now)
    sha256_hash = models.CharField(max_length=512)
    md5_hash = models.CharField(max_length=128)