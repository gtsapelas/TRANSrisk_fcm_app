from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FCM(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')
    map_file = models.CharField(max_length=200)
