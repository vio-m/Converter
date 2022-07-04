from django import forms
from .models import Video

class urlForm(forms.ModelForm):
    url = forms.CharField(label='url', max_length=1000)

    class Meta:
        model = Video
        fields = ('url',)