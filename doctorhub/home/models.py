from django import forms
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
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
from .modules import text_processing, pagination, specialties
from .multilingual.pages.models import MultilingualPage, MonolingualPage


class DigitalTebPageMixin:

    @staticmethod
    def get_home_page():
        return HomePage.objects.first()

    @staticmethod
    def get_blogs_page():
        return ArticlesCategoriesPage.objects.first()

    @staticmethod
    def get_specialists_page():
        return SpecialistsPage.objects.first()


class HomePage(DigitalTebPageMixin, CheckPhoneVerifiedMixin, MultilingualPage):
    subpage_types = [
        'home.ArticlesCategoriesPage',
        'home.SpecialistsPage',
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

    def save(self, *args, **kwargs):
        self.title = 'Home'
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.title = 'Blogs'
        super().save(*args, **kwargs)

    @property
    def template(self):
        return super().get_template_path(ArticlesCategoriesPage)

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
        for child_page in super().child_pages:
            if isinstance(child_page, MonolingualPage):
                if child_page.supports_language():
                    child_pages.append(child_page)
        return child_pages

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = pagination.get_paginated_objects(
            request, self.child_pages
        )
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

    def save(self, *args, **kwargs):
        self.title = self.category.default_name
        super().save(*args, **kwargs)

    @property
    def template(self):
        return super().get_template_path(ArticlesCategoryPage)

    parent_page_types = [
        'home.ArticlesCategoriesPage',
    ]

    subpage_types = [
        'home.ArticlePage',
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

    @property
    def sections_with_title(self):
        sections = []
        for section in self.sections:
            if section.value['title']:
                sections.append(section)
        return sections

    def save(self, *args, **kwargs):
        self.title = text_processing.html_to_str(self.article_title)
        if not self.id:
            super().save(*args, **kwargs)
        self.slug = self.id
        super().save(*args, **kwargs)

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


class SpecialistsPage(
    DigitalTebPageMixin, MetadataPageMixin,
    CheckPhoneVerifiedMixin, ParentPageMixin, MultilingualPage
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.seo_title = translation.gettext('Specialists')
        self.search_description = translation.gettext(
            'Talk to a specialist online, get your medication and health screening packages from wherever you are!'
        )
        return super().serve(request, *args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['specialist_pages'] = pagination.get_paginated_objects(
            request, self.child_pages
        )
        return context

    def save(self, *args, **kwargs):
        self.title = 'Specialists'
        super().save(*args, **kwargs)

    @property
    def translated_title(self):
        return translation.gettext('Specialists')

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.SpecialistPage']


class SpecialistPage(
    DigitalTebPageMixin, MetadataPageMixin,
    CheckPhoneVerifiedMixin, MultilingualPage
):
    user = models.OneToOneField(
        User, blank=False, on_delete=models.SET_NULL, null=True
    )

    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.SpecialistsPage']
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        user_specialties = specialties.get_user_specialties(self.user)
        specialist_name = f'{self.user.first_name} {self.user.last_name}'
        self.seo_title = translation.gettext(
            'Specialists - %(specialties)s - %(specialist_name)s'
        ) % {
            'specialties': text_processing.str_list_to_comma_separated(
                [
                    specialty.name for specialty in user_specialties
                ]
            ),
            'specialist_name': specialist_name
        }
        self.search_description = translation.gettext(
            'Consult %(specialist_name)s via message or video call now.'
        ) % {
            'specialist_name': specialist_name
        }
        return super().serve(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.title = self.user.username
        super().save(*args, **kwargs)
