from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.staticfiles.templatetags.staticfiles import static
from wagtail.images.edit_handlers import ImageChooserPanel

from .work_places.models import *
from ..modules import images
from ..multilingual.mixins import *


class SpecialtyManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = Q(name__icontains=kwargs['name'])
            specialist_name_query = Q(specialist_name__icontains=kwargs['name'])
            qs = qs.filter(
                name_query | specialist_name_query
            )
        return qs


@register_snippet
class Specialty(MultilingualModelMixin, models.Model):
    name = models.TextField()
    specialist_name = models.TextField(default='')
    group = models.OneToOneField(
        Group, on_delete=models.SET_NULL, blank=False, null=True
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image')
            ], heading='Image', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'specialist_name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Specialist Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('group')
            ], heading='Group', classname="collapsible collapsed"
        )
    ]

    @property
    def default_name(self):
        current = languages.get_language_code()
        translation.activate(settings.LANGUAGE_CODE)
        name = self.name
        translation.activate(current)
        return name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Specialties"

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'specialist_name']
        )
        super().save(*args, **kwargs)

    objects = SpecialtyManager()


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


@register_snippet
class Biography(MultilingualModelMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    biography = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Biographies'

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['biography']
        )
        super().save(*args, **kwargs)


@register_snippet
class Education(MultilingualModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=200)
    field = models.CharField(max_length=500)
    institution = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['level', 'field', 'institution']
        )
        super().save(*args, **kwargs)
