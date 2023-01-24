from django import forms
from .models import Video


class urlForm(forms.ModelForm):
    url = forms.CharField(label='url', max_length=1000)
    format = forms.CharField(label='format', max_length=20)

    class Meta:
        model = Video
        fields = ('url', 'format')


class convertForm(forms.ModelForm):
    url = forms.CharField(label='url', max_length=1000)
    quality = forms.CharField(label='quality', max_length=20)
    format = forms.CharField(label='format', max_length=20)

    class Meta:
        model = Video
        fields = ('url', 'quality', 'format')


class titleForm(forms.ModelForm):
    title = forms.CharField(label='title', max_length=1000)

    class Meta:
        model = Video
        fields = ('title',)






