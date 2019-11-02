from wagtail.snippets.models import register_snippet

from ..categories.models import *


@register_snippet
class ArticleCategory(Category):
    square_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    @property
    def icon(self):
        if self.square_image:
            return self.square_image
        else:
            return self.horizontal_image

    panels = Category.panels + [
        ImageChooserPanel('square_image'),
    ]

    class Meta:
        verbose_name_plural = "Article Categories"



