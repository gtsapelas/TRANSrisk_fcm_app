from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField


class Tags(models.Model):
    name = models.CharField(default="",max_length=100,primary_key=True)

# Create your models here.
class FCM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ITAN PROTECT
    country = CountryField()
    status = models.IntegerField(default=1)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    chartis = models.TextField(default = "")
    creation_date = models.DateTimeField('date created')
    map_image = models.ImageField(upload_to='media/images', default='media/images/Capture1.PNG')
    map_html = models.FileField(upload_to='media/html')
    manual = models.BooleanField(default=False)   #  default = None  # allios null=True # false an einai etoimo kai to allazoume an einai manual
    tags = models.ManyToManyField(Tags, related_name='fcm_set')

    def __str__(self):
        return self.title


class FCM_CONCEPT(models.Model):
    fcm = models.ForeignKey(FCM, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    id_in_fcm = models.CharField(max_length=10) # den ksero gt to exoume afisei Charfield
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class FCM_EDGES(models.Model):
    #fcm_concept = models.ForeignKey(FCM_CONCEPT)
    fcm = models.ForeignKey(FCM,null=True, on_delete=models.CASCADE)   # check to null=True
    title = models.CharField(max_length=500)
    id_in_fcm_edges= models.CharField(max_length=10)
    from_node = models.IntegerField(default=0)
    to_node = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class FCM_CONCEPT_INFO(models.Model):
    fcm_concept = models.ForeignKey(FCM_CONCEPT, on_delete=models.CASCADE)
    info = RichTextField()

    def __str__(self):
        return self.info
