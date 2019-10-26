from django.db import models


class Color(models.Model):
    filename = models.CharField(max_length=255, default='filenamedefault')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.filename
