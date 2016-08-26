from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib import admin


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField()

admin.site.register(BlogPost)
