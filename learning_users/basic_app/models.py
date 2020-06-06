from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

    #allows us to access default User things(first name, etc.)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional
    #blank=True means that the user doesn't have to fill it in
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
