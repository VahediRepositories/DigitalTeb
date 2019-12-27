from django.conf import settings
from django.contrib.auth.models import User
from django.utils import translation
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from ..categories.models import *
from ..multilingual.mixins import *


@register_snippet
class ArticleCategory(MultilingualModelMixin, Category):
    horizontal_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    square_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    @property
    def default_name(self):
        current = translation.get_language()
        translation.activate(settings.LANGUAGE_CODE)
        name = self.name
        translation.activate(current)
        return name

    @property
    def icon(self):
        if self.square_image:
            return self.square_image
        else:
            return self.horizontal_image

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'name_{language}')
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                )
            ], heading='Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('horizontal_image'),
                ImageChooserPanel('square_image'),
            ], heading='Image', classname="collapsible collapsed"
        )
    ]

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name']
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Article Categories"


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField(blank=False, default='', max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('date',)

    def __str__(self):
        return self.comment


@register_snippet
class ArticlePageComment(Comment):
    article = ParentalKey(
        'home.ArticlePage', related_name='article_page_comments', on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def children(self):
        return ArticlePageComment.objects.filter(parent=self)

    @property
    def comments(self):
        comments_list = list(self.children)
        for child in self.children:
            comments_list.extend(child.comments)
        return sorted(
            comments_list, key=lambda comment: comment.date
        )

    panels = [
        FieldPanel('owner'),
        FieldPanel('article'),
        FieldPanel('parent'),
        FieldPanel('comment'),
    ]
