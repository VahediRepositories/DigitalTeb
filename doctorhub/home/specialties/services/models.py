from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from ...multilingual.mixins import MultilingualModelMixin
from ...modules import images


class LabelManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = Q(name__icontains=kwargs['name'])
            description_query = Q(description__icontains=kwargs['name'])
            qs = qs.filter(
                name_query | description_query
            )
        return qs


class Label(MultilingualModelMixin, models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to='services_images', null=True, blank=True
    )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return static(HOSPITAL_ICON)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'description']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    def make_square_image(self):
        if self.image:
            images.make_square_image(self.image.path)

    def compress_image(self):
        if self.image:
            images.compress_image(self.image.path)

    objects = LabelManager()
