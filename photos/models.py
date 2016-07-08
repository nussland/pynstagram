import os

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='%Y/%m/%d', blank=True, null=True)
    thumb = models.ImageField(upload_to='%Y/%m/%d/thumb', blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk', )

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('photos:view_photo', kwargs={'pk':self.pk})


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    memo = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=Photo)
def create_thumbnail(sender, **kwargs):
    instance = kwargs.pop('instance')

    if not instance.image:
        return

    if instance.thumb:
        return

    from PIL import Image
    from io import BytesIO
    from django.core.files.uploadedfile import SimpleUploadedFile

    thumb_size = (200,200)

    if instance.image.name.endswith(".jpg"):
        PIL_TYPE = 'jpeg'
        DJANGO_TYPE = 'image/jpeg'
        FILE_EXT = 'jpg'
    elif instance.image.name.endswith(".png"):
        PIL_TYPE = 'png'
        DJANGO_TYPE = 'image/png'
        FILE_EXT = 'png'

    image = Image.open(BytesIO(instance.image.read()))
    image.thumbnail(thumb_size, Image.ANTIALIAS)

    fp = BytesIO()
    image.save(fp, PIL_TYPE)
    fp.seek(0)

    suf = SimpleUploadedFile(os.path.split(instance.image.name)[-1], fp.read(), content_type=DJANGO_TYPE)
    instance.thumb.save('{}_thumb.{}'.format(os.path.splitext(suf.name)[0], FILE_EXT), suf, save=False)


@receiver(post_delete, sender=Photo)
def delete_attached_image(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.image.delete(save=False)
    instance.thumb.delete(save=False)

