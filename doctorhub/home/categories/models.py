from django.db import models


class Category(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
