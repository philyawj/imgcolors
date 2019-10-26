from django.db import models
from django.utils import timezone


class Color(models.Model):
    filename = models.CharField(max_length=255, default='filenamedefault')
    image = models.ImageField(upload_to='images/')
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.filename
