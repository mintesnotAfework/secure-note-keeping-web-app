from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user_user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile/user",default="profile/default/default.png")
    hashed_password = models.BinaryField()
    # signed_password = models.BinaryField()
    file_path = models.CharField(max_length=256)
