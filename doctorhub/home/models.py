from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.urls import reverse
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import StreamFieldPanel, RichTextFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .accounts.phone.mixins import CheckPhoneVerifiedMixin
from .articles.blocks import *
from .articles.forms import *
from .articles.models import *
from .articles.serializers import *
from .mixins import *
from .modules import text_processing, pagination
from .modules.specialties import specialties
from .multilingual.pages.models import MultilingualPage, MonolingualPage
from .specialties.models import *
from .specialties.work_places.models import *


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
        return HttpResponseRedirect(
            self.get_specialists_page().get_url()
        )

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
        on_delete=models.PROTECT, null=True
    )

    content_panels = [
        SnippetChooserPanel('category'),
    ]

    promote_panels = []
    settings_panels = []

    @property
    def specialists_page(self):
        for child in super().child_pages:
            if isinstance(child, SpecialistsArticlesCategoryPage):
                return child
        new_page = SpecialistsArticlesCategoryPage()
        self.add_child(instance=new_page)
        new_page.save()
        return new_page

    @property
    def child_pages(self):
        child_pages = []
        for child_page in super().child_pages:
            if isinstance(child_page, MonolingualPage):
                if child_page.supports_language():
                    child_pages.append(child_page)
        return child_pages

    @property
    def articles(self):
        return [
            child_page
            for child_page in self.child_pages
        ]

    @property
    def specialists_articles(self):
        return [
            child_page
            for child_page in self.child_pages
            if child_page.written_by_specialist
        ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['articles'] = pagination.get_paginated_objects(
            request, self.articles
        )
        context['specialists_articles'] = self.specialists_articles[:2]
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
        'home.SpecialistsArticlesCategoryPage',
    ]


class SpecialistsArticlesCategoryPage(
    DigitalTebPageMixin, MetadataPageMixin,
    CheckPhoneVerifiedMixin, ParentPageMixin, MultilingualPage
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.search_description = translation.gettext(
            "Articles written by specialists about %(category)s"
        ) % {
                                      'category': self.category.name
                                  }
        self.seo_title = translation.gettext(
            'Blogs - %(category)s - Specialists'
        ) % {
                             'category': self.category.name
                         }
        self.search_image = self.category.icon
        return super().serve(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.title = "Specialists"
        super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['articles'] = pagination.get_paginated_objects(
            request, self.articles
        )
        return context

    @property
    def articles(self):
        return self.get_parent().specific.specialists_articles

    @property
    def category(self):
        return self.get_parent().specific.category

    @property
    def template(self):
        return super().get_template_path(SpecialistsArticlesCategoryPage)

    parent_page_types = [
        'home.ArticlesCategoryPage',
    ]

    subpage_types = []


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

    def get_edit_url(self):
        return reverse(
            'wagtailadmin_pages:edit', args=(self.pk,)
        )

    @property
    def written_by_specialist(self):
        if self.owner:
            return specialties.is_specialist(self.owner)
        else:
            return False

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
                                 # FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
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


class RTLArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_page_rtl_tags', on_delete=models.CASCADE
    )


class LTRArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_page_ltr_tags', on_delete=models.CASCADE
    )


class ArticlePage(Article):
    # categories = ParentalManyToManyField(ArticleCategory, blank=False)
    rtl_tags = ClusterTaggableManager(
        through=RTLArticlePageTag, blank=True, related_name='rtl_tags',
        help_text='Tags in "right to left" languages like: Persian, Arabic, Hebrew and ...'
    )
    ltr_tags = ClusterTaggableManager(
        through=LTRArticlePageTag, blank=True, related_name='ltr_tags',
        help_text='Tags in "left to right" languages like: English, French, Spanish and ...'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=False, on_delete=models.PROTECT, related_name='+'
    )

    def hit_count(self, request):
        hit_count = HitCount.objects.get_for_object(self)
        HitCountMixin.hit_count(request, hit_count)

    def serve(self, request, *args, **kwargs):
        self.hit_count(request)
        return super().serve(request, *args, **kwargs)

    promote_panels = []
    settings_panels = []

    @property
    def manager(self):
        return ArticlePage.objects

    @property
    def template(self):
        return self.get_template_path(ArticlePage)

    @property
    def comments(self):
        return self.article_page_comments.filter(parent=None)

    parent_page_types = ['home.ArticlesCategoryPage']
    subpage_types = []


class SpecialistsPage(
    DigitalTebPageMixin, MetadataPageMixin,
    ParentPageMixin, MultilingualPage
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    def serve(self, request, *args, **kwargs):
        self.seo_title = translation.gettext('Medicare Specialists')
        self.search_description = translation.gettext(
            # 'Talk to a specialist online, get your medication and health screening packages from wherever you are!'
            'Find out everything about specialists, medical centers, equipments, ...'
        )
        return super().serve(request, *args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['specialists'] = pagination.get_paginated_objects(
            request, self.specialists
        )
        return context

    @property
    def specialists(self):
        return [
            child_page for child_page in self.child_pages if isinstance(child_page, SpecialistPage)
        ]

    def save(self, *args, **kwargs):
        self.title = 'Specialists'
        super().save(*args, **kwargs)

    @property
    def translated_title(self):
        return translation.gettext('Specialists')

    parent_page_types = ['home.HomePage']
    subpage_types = [
        'home.SpecialistPage',
        'home.SpecialtyPage',
    ]

    @property
    def template(self):
        return super().get_template_path(SpecialistsPage)


class MedicalCentersPage(
    DigitalTebPageMixin, MetadataPageMixin, ParentPageMixin, MultilingualPage
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    def serve(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.seo_title = translation.gettext('Medical Centers')
        self.search_description = translation.gettext(
            # 'Talk to a specialist online, get your medication and health screening packages from wherever you are!'
            'Find out everything about medical centers, specialists, equipments, ...'
        )
        return super().serve(request, *args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['places'] = pagination.get_paginated_objects(
            request, self.places
        )
        return context

    @property
    def places(self):
        return [
            child_page for child_page in self.child_pages if isinstance(child_page, WorkPlacePage)
        ]

    def save(self, *args, **kwargs):
        self.title = 'Medical Centers'
        super().save(*args, **kwargs)

    @property
    def translated_title(self):
        return translation.gettext('Medical Centers')

    parent_page_types = ['home.HomePage']
    subpage_types = [
        'home.WorkPlacePage',
        'home.MedicalCenterPage',
    ]

    @property
    def template(self):
        return super().get_template_path(SpecialistsPage)


class SpecialtyPage(
    DigitalTebPageMixin, MetadataPageMixin, MultilingualPage
):
    specialty = models.OneToOneField(
        Specialty, blank=False,
        on_delete=models.PROTECT, null=True
    )

    content_panels = [
        SnippetChooserPanel('specialty'),
    ]
    promote_panels = []
    settings_panels = []

    @property
    def specialists(self):
        return [
            specialist
            for specialist in self.get_parent().specific.specialists
            if self.specialty in specialties.get_user_specialties(
                specialist.user
            )
        ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['specialists'] = pagination.get_paginated_objects(
            request, self.specialists
        )
        return context

    def serve(self, request, *args, **kwargs):
        self.seo_title = translation.gettext(
            'Medicare Specialists - %(specialty)s'
        ) % {
                             'specialty': self.specialty.name
                         }
        self.search_description = translation.gettext(
            'Find out everything about %(specialty)s: specialists, medical centers, equipments, ...'
        ) % {
                                      'specialty': self.specialty.name
                                  }
        return super().serve(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.title = self.specialty.default_name
        super().save(*args, **kwargs)

    @property
    def template(self):
        return super().get_template_path(SpecialtyPage)

    parent_page_types = ['home.SpecialistsPage']
    subpage_types = []


class MedicalCenterPage(
    DigitalTebPageMixin, MetadataPageMixin, ParentPageMixin, MultilingualPage
):
    medical_center = models.OneToOneField(
        MedicalCenter, blank=False,
        on_delete=models.PROTECT, null=True
    )

    content_panels = [
        SnippetChooserPanel('medical_center'),
    ]
    promote_panels = []
    settings_panels = []

    @property
    def places(self):
        return [
            place
            for place in self.get_parent().specific.places
            if self.medical_center == place.medical_center
        ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['places'] = pagination.get_paginated_objects(
            request, self.places
        )
        return context

    def serve(self, request, *args, **kwargs):
        self.seo_title = translation.gettext(
            'Medical Centers - %(medical_centers)s'
        ) % {
                             'medical_centers': self.medical_center.plural_name
                         }
        self.search_description = translation.gettext(
            'Find out everything about %(medical_centers)s: specialists, equipments, ...'
        ) % {
                                      'medical_centers': self.medical_center.plural_name
                                  }
        return super().serve(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.title = self.medical_center.default_plural_name
        super().save(*args, **kwargs)


class SpecialistPage(
    DigitalTebPageMixin, MetadataPageMixin,
    MultilingualPage
):
    user = models.OneToOneField(
        User, blank=False, on_delete=models.PROTECT, null=True
    )

    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.SpecialistsPage']
    subpage_types = []

    def hit_count(self, request):
        hit_count = HitCount.objects.get_for_object(self)
        HitCountMixin.hit_count(request, hit_count)

    def serve(self, request, *args, **kwargs):
        user_specialties = specialties.get_user_specialties(self.user)
        specialist_name = f'{self.user.profile.first_name} {self.user.profile.last_name}'
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
            # 'Consult %(specialist_name)s via message or video call now.'
            'Everything about %(specialist_name)s: services, work places, ...'
        ) % {
                                      'specialist_name': specialist_name
                                  }
        self.hit_count(request)
        return super().serve(request, *args, **kwargs)

    @property
    def articles(self):
        articles = ArticlePage.objects.filter(
            owner=self.user
        ).live().public().order_by('-first_published_at')
        return [
            article for article in articles
            if isinstance(article, MonolingualPage) and article.supports_language()
        ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['articles'] = pagination.get_paginated_objects(
            request, self.articles, page_size=3
        )
        return context

    def save(self, *args, **kwargs):
        self.title = self.user.username
        self.slug = self.user.pk
        super().save(*args, **kwargs)

    @property
    def template(self):
        return super().get_template_path(SpecialistPage)


class WorkPlacePage(
    DigitalTebPageMixin, MetadataPageMixin, MultilingualPage
):
    place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, null=True, blank=False)

    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.MedicalCentersPage']
    subpage_types = []

    def hit_count(self, request):
        hit_count = HitCount.objects.get_for_object(self)
        HitCountMixin.hit_count(request, hit_count)

    def save(self, *args, **kwargs):
        self.title = self.place.name
        self.slug = self.place.pk
        super().save(*args, **kwargs)

    @property
    def template(self):
        return super().get_template_path(SpecialistPage)
