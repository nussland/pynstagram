from django import forms


from .models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        field = ['title', 'content', 'image', ]