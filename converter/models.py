from django.db import models


class Video(models.Model):
    storage = models.ImageField(upload_to="static/media/")
    title = models.CharField(max_length=120)
    typ = models.CharField(max_length=20, default="mp3")
    url = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.title}.{self.typ}'
