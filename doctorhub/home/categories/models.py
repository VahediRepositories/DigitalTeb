from django.db import models


CATEGORY_NAME_MAX_LENGTH = 200


class Category(models.Model):
    name = models.CharField(default='', max_length=CATEGORY_NAME_MAX_LENGTH)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
