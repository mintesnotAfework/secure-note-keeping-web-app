from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class FileModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    content = models.BinaryField()
    date_time = models.DateTimeField(default=now)
    sha512_hash = models.BinaryField()
    md5_hash = models.BinaryField()