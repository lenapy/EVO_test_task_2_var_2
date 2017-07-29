from django.db import models


class FileName(models.Model):
    name = models.CharField(max_length=50)
