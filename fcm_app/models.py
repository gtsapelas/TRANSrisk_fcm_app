from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class FCM(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    creation_date = models.DateTimeField('date created')
    map_image = models.ImageField(upload_to='media/images')
    map_html = models.FileField(upload_to='media/html')

