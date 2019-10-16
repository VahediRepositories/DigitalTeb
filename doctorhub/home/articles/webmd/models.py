from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Topic(models.Model):
    farsi_name = models.TextField()
    english_name = models.TextField()

    panels = [
        FieldPanel('farsi_name'),
        FieldPanel('english_name'),
    ]

    def __str__(self):
        return self.english_name
