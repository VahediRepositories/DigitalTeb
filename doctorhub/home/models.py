import uuid

from django import forms
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import StreamFieldPanel, RichTextFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .accounts.phone.mixins import CheckPhoneVerifiedMixin
from .articles.blocks import *
from .articles.models import *
from .articles.serializers import *
from .mixins import *
from .modules import text_processing
from .multilingual.pages.models import MultilingualPage, MonolingualPage


class DigitalTebPageMixin:

    def __init__(self, *args, **kwargs):
        super(DigitalTebPageMixin, self).__init__(*args, **kwargs)
        self.messages_links = {}

    @staticmethod
    def get_home_page():
        return HomePage.objects.first()

    @staticmethod
    def get_blogs_page():
        return ArticlesCategoriesPage.objects.first()


class HomePage(DigitalTebPageMixin, CheckPhoneVerifiedMixin, MultilingualPage):
    subpage_types = [
        'home.ArticlesCategoriesPage',
    ]

    settings_panels = []
    promote_panels = []
    content_panels = []

    def serve(self, request, *args, **kwargs):
        blogs_page = self.get_blogs_page()
        return HttpResponseRedirect(blogs_page.get_url())

    @property
    def translated_title(self):
        return translation.gettext('Home')

    def clean(self):
        super(HomePage, self).clean()
        self.title = 'Home'
        self.slug = slugify(self.title)


class ArticlesCategoriesPage(
    DigitalTebPageMixin,
    MetadataPageMixin, CheckPhoneVerifiedMixin,
    ParentPageMixin, MultilingualPage
):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ArticlesCategoryPage']

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        categories = [page.category.name for page in self.child_pages]
        self.search_description = text_processing.str_list_to_comma_separated(categories)
        self.seo_title = translation.gettext('Blogs')
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super(ArticlesCategoriesPage, self).clean()
        self.title = 'Blogs'
        self.slug = slugify(self.title)

    @property
    def template(self):
        return super(ArticlesCategoriesPage, self).template

    @property
    def translated_title(self):
        return translation.gettext('Blogs')

    content_panels = []
    promote_panels = []
    settings_panels = []


class ArticlesCategoryPage(
    DigitalTebPageMixin, MetadataPageMixin,
    CheckPhoneVerifiedMixin, ParentPageMixin, MultilingualPage
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

    @property
    def child_pages(self):
        child_pages = []
        for child_page in super(ArticlesCategoryPage, self).child_pages:
            if isinstance(child_page, MonolingualPage):
                if child_page.supports_language():
                    child_pages.append(child_page)
        return child_pages

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        children = self.child_pages
        paginator = Paginator(children, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.search_description = translation.gettext(
            'Everything about %(category)s'
        ) % {
                                      'category': self.category.name
                                  }
        self.seo_title = translation.gettext(
            'Blogs - %(category)s'
        ) % {
                             'category': self.category.name
                         }
        self.search_image = self.category.icon
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super(ArticlesCategoryPage, self).clean()
        if self.category:
            self.title = self.category.default_name
            self.slug = slugify(self.title)

    @property
    def template(self):
        return super(ArticlesCategoryPage, self).template

    parent_page_types = [
        'home.ArticlesCategoriesPage',
    ]

    subpage_types = [
        'home.ArticlePage',
        'home.WebMDBlogPost',
    ]


class Article(
    DigitalTebPageMixin, MetadataPageMixin, CheckPhoneVerifiedMixin,
    TaggedPageMixin, MonolingualPage
):
    article_title = RichTextField(
        features=[],
        blank=False, null=True,
    )
    article_summary = RichTextField(
        features=configurations.BASIC_RICHTEXT_FEATURES, blank=False, null=True,
    )
    article_introduction = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
    )
    article_conclusion = RichTextField(
        features=configurations.BASIC_RICHTEXT_FEATURES, blank=True, null=True,
    )
    sections = StreamField(
        [
            ('section', SectionBlock()),
        ], blank=False
    )

    uuid4 = models.TextField(default='')

    @property
    def sections_with_title(self):
        sections = []
        for section in self.sections:
            if section.value['title']:
                sections.append(section)
        return sections

    def clean(self):
        super(Article, self).clean()
        if not self.id:
            self.refresh_slug()
        if self.article_title:
            self.title = text_processing.html_to_str(self.article_title)
        # self.search_image = self.image

    def refresh_slug(self):
        self.set_uuid4()
        self.slug = '{}-'.format(
            type(self).__name__
        ) + self.uuid4

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        if self.sections_with_title:
            self.search_description = translation.gettext(
                '%(article_title)s including %(article_sections)s'
            ) % {
                                          'article_title': self.title,
                                          'article_sections': text_processing.str_list_to_comma_separated(
                                              [
                                                  text_processing.html_to_str(section.value['title'].source)
                                                  for section in self.sections_with_title
                                              ]
                                          )
                                      }
        else:
            self.search_description = self.title
        self.seo_title = translation.gettext(
            'Blogs - %(category)s - %(article_title)s'
        ) % {
                             'category': self.get_parent().specific.category.name,
                             'article_title': self.title
                         }
        return super().serve(request, *args, **kwargs)

    def set_uuid4(self):
        uuid4 = uuid.uuid4()
        while self.manager.filter(uuid4=uuid4).exists():
            uuid4 = uuid.uuid4()
        self.uuid4 = str(uuid4)

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
                     ] + TaggedPageMixin.tags_panel + [
                         MonolingualPage.language_panel
                     ]

    class Meta:
        abstract = True
        ordering = [
            'first_published_at'
        ]


class RTLArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_page_rtl_tags', on_delete=models.CASCADE
    )


class LTRArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_page_ltr_tags', on_delete=models.CASCADE
    )


class ArticlePage(Article):
    categories = ParentalManyToManyField(ArticleCategory, blank=False)
    rtl_tags = ClusterTaggableManager(
        through=RTLArticlePageTag, blank=True, related_name='rtl_tags'
    )
    ltr_tags = ClusterTaggableManager(
        through=LTRArticlePageTag, blank=True, related_name='ltr_tags'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

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

    @property
    def manager(self):
        return ArticlePage.objects

    @property
    def template(self):
        return self.get_template_path(ArticlePage)

    parent_page_types = ['home.ArticlesCategoryPage']
    subpage_types = []


class RTLWebMDBlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebMDBlogPost', related_name='webmd_blog_post_rtl_tags', on_delete=models.CASCADE
    )


class LTRWebMDBlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebMDBlogPost', related_name='webmd_blog_post_ltr_tags', on_delete=models.CASCADE
    )


class WebMDBlogPost(Article):
    categories = ParentalManyToManyField(ArticleCategory, blank=False)
    rtl_tags = ClusterTaggableManager(
        through=RTLWebMDBlogPostTag, blank=True, related_name='webmd_rtl_tags'
    )
    ltr_tags = ClusterTaggableManager(
        through=LTRWebMDBlogPostTag, blank=True, related_name='webmd_ltr_tags'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.ArticlesCategoryPage']
    subpage_types = []

    @property
    def manager(self):
        return WebMDBlogPost.objects

    @property
    def template(self):
        return self.get_template_path(WebMDBlogPost)
