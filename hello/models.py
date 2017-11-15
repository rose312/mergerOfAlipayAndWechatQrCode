# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
import os

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Img(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)

# def delete_file(sender, **kwargs):
#     patch = kwargs['instance']
#     os.remove(patch.filename.path)
#     print("删除")
#
# post_delete.connect(delete_file, Img)