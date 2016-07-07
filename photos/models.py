import os

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='%Y/%m/%d', blank=True, null=True)
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/thumbnails", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk', )

    def get_absolute_url(self):
        return reverse('photos:view_photo', kwargs={'pk':self.pk})

    def create_thumbnail(self):
        if not self.image:
            return

        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        thumb_size = (200,200)

        if self.image.name.endswith(".jpg"):
            PIL_TYPE = 'jpeg'
            DJANGO_TYPE = 'image/jpeg'
        elif self.image.name.endswith(".png"):
            PIL_TYPE = 'png'
            DJANGO_TYPE = 'image/png'

        file_name, file_ext = os.path.splitext(self.image.name)
        image = Image.open(BytesIO(self.image.read()))
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        fp = BytesIO()
        image.save(fp, PIL_TYPE)
        fp.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], fp.read(), content_type=DJANGO_TYPE)
        self.thumbnail.save('{}_thumnail.{}'.format(file_name, file_ext), suf, save=False)

    def save(self):
        self.create_thumbnail()
        super(Photo, self).save()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    memo = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
