from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class FCM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ITAN PROTECT
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    chartis = models.TextField(default = "")
    creation_date = models.DateTimeField('date created')
    map_image = models.ImageField(upload_to='media/images', default='media/images/Capture1.PNG')
    map_html = models.FileField(upload_to='media/html')
    manual = models.BooleanField(default=False)   #  default = None  # allios null=True # false an einai etoimo kai to allazoume an einai manual

    def __str__(self):
        return self.title


class FCM_CONCEPT(models.Model):
    fcm = models.ForeignKey(FCM)  # MIPOS PREPEI NA TO AFISOUME fcm  ???
    title = models.CharField(max_length=200)
    id_in_fcm = models.CharField(max_length=10) # den ksero gt to exoume afisei Charfield
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class FCM_EDGES(models.Model):
    fcm_concept = models.ForeignKey(FCM_CONCEPT)
    title = models.CharField(max_length=200)
    id_in_fcm_edges= models.CharField(max_length=10)
    from_node = models.IntegerField(default=0)
    to_node = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class FCM_CONCEPT_INFO(models.Model):
    fcm_concept = models.ForeignKey(FCM_CONCEPT)
    info = RichTextField()

    def __str__(self):
        return self.info
