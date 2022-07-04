from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=120)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.title}'
