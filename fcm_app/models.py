from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class FCM(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    creation_date = models.DateTimeField('date created')
    map_image = models.ImageField(upload_to='media/images')
    map_html = models.FileField(upload_to='media/html')

    def __str__(self):
        return self.title


class FCM_CONCEPT(models.Model):
    fcm = models.ForeignKey(FCM)  # MIPOS PREPEI NA TO AFISOUME fcm  ???
    title = models.CharField(max_length=200)
    id_in_fcm = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class FCM_CONCEPT_INFO(models.Model):
    fcm_concept = models.ForeignKey(FCM_CONCEPT)
    info = RichTextField()

    def __str__(self):
        return self.info
