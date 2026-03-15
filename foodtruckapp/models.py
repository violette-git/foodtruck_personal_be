from django.db import models
from user_app.models import User




# Create your models here.

class Email_List(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', blank=False, null=False)

    name = models.CharField(max_length=50)

    number = models.CharField(max_length=20)

    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    email = models.EmailField()

    coupon_count = models.IntegerField(default=0)

    def __str__(self):

        return f'{self.name.capitalize()}'
