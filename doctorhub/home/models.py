import uuid

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel, RichTextFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .articles.blocks import *
from .articles.models import *
from .articles.serializers import *
from .modules import list_processing
from .modules import text_processing


class DigitalTebPageMixin:

    @staticmethod
    def get_home_page():
        return HomePage.objects.first()


class HomePage(DigitalTebPageMixin, Page):
    subpage_types = [
        'home.ArticlesCategoriesPage'
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect('/articles/')


class ArticlesCategoriesPage(
    DigitalTebPageMixin, MetadataPageMixin, Page
):
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

    def get_row_categories(self):
        children = self.get_children().live().public()
        return list_processing.list_to_sublists_of_size_n(children, 2)

    content_panels = []
    promote_panels = []
    settings_panels = []


class ArticlesCategoryPage(
    DigitalTebPageMixin, MetadataPageMixin, Page
):
    category = models.OneToOneField(
        ArticleCategory, blank=False,
        on_delete=models.SET_NULL, null=True
    )

    content_panels = [
        SnippetChooserPanel('category'),
    ]

    promote_panels = []
    settings_panels = []

    @staticmethod
    def get_row_articles(posts):
        return list(
            reversed(list_processing.list_to_sublists_of_size_n(posts, 2))
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        children = self.get_children().live().public()
        paginator = Paginator(children, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['row_articles'] = self.get_row_articles(posts)
        context['posts'] = posts
        return context

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
        if self.category:
            self.title = self.category.farsi_name
            self.slug = slugify(self.category.english_name)
            self.search_image = self.category.horizontal_image

    parent_page_types = [
        'home.ArticlesCategoriesPage',
    ]

    subpage_types = [
        'home.ArticlePage',
        'home.WebMDBlogPost',
    ]


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_tags', on_delete=models.CASCADE
    )


class ArticleEnglishTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_english_tags', on_delete=models.CASCADE
    )


class ArticlePage(DigitalTebPageMixin, MetadataPageMixin, Page):
    categories = ParentalManyToManyField(ArticleCategory, blank=False)
    tags = ClusterTaggableManager(
        through=ArticleTag, blank=True, related_name='farsi_tags'
    )
    english_tags = ClusterTaggableManager(
        through=ArticleEnglishTag, blank=True, related_name='english_tags'
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
            ], heading='Details', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                RichTextFieldPanel('article_summary'),
                RichTextFieldPanel('article_introduction'),
                StreamFieldPanel('sections'),
                RichTextFieldPanel('article_conclusion'),
            ], heading='Content', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('tags'),
            ], heading='Tags', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('english_tags'),
            ], heading='English Tags', classname='collapsible collapsed'
        ),
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

    def has_sections_with_title(self):
        for section in self.sections:
            if section.value['title']:
                return True

    def clean(self):
        super().clean()
        if not self.id:
            self.set_uuid4()
            self.slug = 'article-' + self.uuid4
        if self.article_title:
            self.title = text_processing.html_to_str(self.article_title)
        self.search_image = self.image

    def serve(self, request, *args, **kwargs):
        self.search_description = self.title + ' شامل ' + text_processing.str_list_to_comma_separated(
            [
                text_processing.html_to_str(section.value['title'].source)
                for section in self.sections
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

    @property
    def farsi_tags(self):
        return self.tags

    parent_page_types = ['home.ArticlesCategoryPage']
    subpage_types = []

    class Meta:
        ordering = [
            '-first_published_at'
        ]


class WebMDBlogPostFarsiTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebMDBlogPost', related_name='webmd_farsi_tags', on_delete=models.CASCADE
    )


class WebMDBlogPostEnglishTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebMDBlogPost', related_name='webmd_english_tags', on_delete=models.CASCADE
    )


class WebMDBlogPost(DigitalTebPageMixin, MetadataPageMixin, Page):
    categories = ParentalManyToManyField(ArticleCategory, blank=False)
    farsi_tags = ClusterTaggableManager(
        through=WebMDBlogPostFarsiTag, blank=True, related_name='webmd_farsi_tags'
    )
    english_tags = ClusterTaggableManager(
        through=WebMDBlogPostEnglishTag, blank=True, related_name='webmd_english_tags'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality horizontal image',
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
            ], heading='Details', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                RichTextFieldPanel('article_summary'),
                RichTextFieldPanel('article_introduction'),
                StreamFieldPanel('sections'),
                RichTextFieldPanel('article_conclusion'),
            ], heading='Content', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_tags'),
            ], heading='Farsi Tags', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('english_tags'),
            ], heading='English Tags', classname='collapsible collapsed'
        ),
    ]
    promote_panels = []
    settings_panels = []

    def has_sections_with_title(self):
        for section in self.sections:
            if section.value['title']:
                return True

    def clean(self):
        super().clean()
        if not self.id:
            self.set_uuid4()
            self.slug = 'webmd-article-' + self.uuid4
        if self.article_title:
            self.title = text_processing.html_to_str(self.article_title)
        self.search_image = self.image

    def serve(self, request, *args, **kwargs):
        self.search_description = self.title + ' شامل ' + text_processing.str_list_to_comma_separated(
            [
                text_processing.html_to_str(section.value['title'].source)
                for section in self.sections
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
