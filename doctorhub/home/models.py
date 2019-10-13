import uuid

from django import forms
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel, RichTextFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .articles.blocks import *
from .articles.models import *
from .articles.serializers import *
from .modules import list_processing
from .modules import text_processing


class HomePage(Page):
    subpage_types = [
        'home.ArticlesCategoriesPage'
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect('/articles/')


class ArticlesCategoriesPage(MetadataPageMixin, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ArticlesCategoryPage']

    def serve(self, request, *args, **kwargs):
        children = self.get_children().live()
        categories = [page.specific.category.farsi_name for page in children]
        self.search_description = 'مقالات ' + text_processing.str_list_to_comma_separated(categories)
        self.seo_title = 'مقالات'
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        self.title = 'مقالات'
        self.slug = 'articles'

    def get_home_page(self):
        return self.get_parent().specific

    def get_row_categories(self):
        children = self.get_children().live()
        return list_processing.list_to_sublists_of_size_n(children, 2)

    content_panels = []
    promote_panels = []
    settings_panels = []


class ArticlesCategoryPage(MetadataPageMixin, Page):
    category = models.OneToOneField(
        ArticleCategory, blank=False,
        on_delete=models.SET_NULL, null=True
    )

    content_panels = [
        SnippetChooserPanel('category'),
    ]

    promote_panels = []
    settings_panels = []

    def get_row_articles(self):
        children = self.get_children().live()
        return list(
            reversed(list_processing.list_to_sublists_of_size_n(children, 2))
        )

    def serve(self, request, *args, **kwargs):
        self.search_description = 'مقالات حوزه ى {}'.format(
            self.category.farsi_name
        )
        self.seo_title = 'مقالات - {}'.format(
            self.category.farsi_name
        )
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        self.title = self.category.farsi_name
        self.slug = slugify(self.category.english_name)
        self.search_image = self.category.square_image

    parent_page_types = [
        'home.ArticlesCategoriesPage',
    ]

    subpage_types = [
        'home.ArticlePage',
    ]

    def get_home_page(self):
        return self.get_parent().specific.get_home_page()


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_tags', on_delete=models.CASCADE
    )


class ArticlePage(MetadataPageMixin, Page):
    categories = ParentalManyToManyField(ArticleCategory, blank=False)
    tags = ClusterTaggableManager(
        through=ArticleTag, blank=True
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    article_title = RichTextField(
        features=[], blank=False, null=True,
        help_text='It has to start with a farsi word'
    )
    article_summary = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=False, null=True,
        help_text='It has to start with a farsi word'
    )
    article_introduction = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
        help_text='It has to start with a farsi word'
    )
    article_conclusion = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
        help_text='It has to start with a farsi word'
    )
    sections = StreamField(
        [
            ('section', SectionBlock()),
        ], blank=True
    )

    content_panels = [
        MultiFieldPanel(
            [
                RichTextFieldPanel('article_title'),
                ImageChooserPanel('image'),
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
                FieldPanel('tags'),
            ], heading='Details', classname="collapsible collapsed"),
        MultiFieldPanel(
            [
                RichTextFieldPanel('article_summary'),
                RichTextFieldPanel('article_introduction'),
                StreamFieldPanel('sections'),
                RichTextFieldPanel('article_conclusion'),
            ], heading='Content', classname="collapsible collapsed"),
    ]
    promote_panels = []
    settings_panels = []

    # api_fields = [
    #     APIField('categories', serializer=ArticleCategoriesField()),
    #     APIField('tags'),
    #     APIField('image', serializer=ImageRenditionField(
    #         'fill-2000x2000-c80|jpegquality-100')
    #              ),
    #     APIField('article_summary'),
    #     APIField('article_introduction'),
    #     APIField('article_conclusion'),
    #     APIField('paragraphs', serializer=ParagraphsField()),
    # ]

    def get_home_page(self):
        return self.get_parent().specific.get_home_page()

    def clean(self):
        super().clean()
        if not self.id:
            self.set_uuid4()
            self.slug = 'article-' + self.uuid4
        self.title = text_processing.html_to_str(self.article_title)
        self.search_image = self.image

    def serve(self, request, *args, **kwargs):
        self.search_description = self.title + ' شامل ' + text_processing.str_list_to_comma_separated(
            [
                text_processing.html_to_str(paragraph.value['title'].source)
                for paragraph in self.sections
            ]
        )
        self.seo_title = 'مقالات - {} - {}'.format(
            self.get_parent().specific.category.farsi_name,
            self.title
        )
        return super().serve(request, *args, **kwargs)

    uuid4 = models.TextField(default='')

    def set_uuid4(self):
        uuid4 = uuid.uuid4()
        while ArticlePage.objects.filter(uuid4=uuid4).exists():
            uuid4 = uuid.uuid4()
        self.uuid4 = str(uuid4)

    parent_page_types = ['home.ArticlesCategoryPage']
    subpage_types = []

    class Meta:
        ordering = [
            '-first_published_at'
        ]
