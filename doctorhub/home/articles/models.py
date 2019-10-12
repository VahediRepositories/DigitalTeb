from wagtail.snippets.models import register_snippet

from ..categories.models import *


@register_snippet
class ArticleCategory(Category):
    farsi_description = models.TextField(default='')

    panels = Category.panels + [
        FieldPanel('farsi_description'),
    ]

    class Meta:
        verbose_name_plural = "Article Categories"



