from django.db import models
from django.conf import settings


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True)
    modified_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    memo = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_created=True)
    modified_at = models.DateTimeField(auto_now=True)
