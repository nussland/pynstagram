from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


from .models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'content', ]