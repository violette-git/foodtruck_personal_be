from email.policy import default
from django.db import models
from PIL import Image
from user_app.models import User




# Create your models here.

class Email_List(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', blank=False, null=False )
    
    name = models.CharField(max_length=50)

    number = models.IntegerField()

    profile_pic = models.ImageField()

    email = models.URLField()

    coupon_count = models.IntegerField(default=0)

    def __str__(self):

        return f'{self.name.capitalize()}'

    def __self__(self):

        return f'{self.name.capitalize()}'