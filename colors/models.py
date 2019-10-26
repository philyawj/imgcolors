from django.db import models


class Color(models.Model):
    image = models.ImageField(upload_to='images/')
