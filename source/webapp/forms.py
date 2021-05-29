from django import forms
from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo_img', 'signature', 'album']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description']
