from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import translation
from notifications.signals import notify
from notifications.models import *

from ...images.mixins import SquareIconMixin
from ...images.models import SquareIcon
from ...locations.cities.models import *


class MedicalCenterManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_queryset()
        name = kwargs.get('name', '')
        if name:
            name_query = languages.multilingual_field_search('name', name)
            plural_name_query = languages.multilingual_field_search('plural_name', name)
            qs = qs.filter(
                name_query | plural_name_query
            )
        return qs


@register_snippet
class MedicalCenter(SquareIcon, MultilingualModelMixin, models.Model):
    name = models.CharField(max_length=100)
    plural_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    panels = SquareIcon.panels + [
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
                        FieldPanel(f'plural_name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Plural Name', classname="collapsible collapsed"
        ),
    ]

    @property
    def default_plural_name(self):
        return self.get_default_field('plural_name')

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'plural_name']
        )
        super().save(*args, **kwargs)

    objects = MedicalCenterManager()


@register_snippet
class WorkPlaceDefaultIcon(SquareIcon):
    pass


class WorkPlaceManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        name = kwargs.get('name', '')
        city = kwargs.get('city', '')
        if city:
            qs = qs.filter(
                city__in=City.objects.search(name=city)
            )
        if name:
            medical_center_query = languages.multilingual_field_search(
                'medical_center__name', name
            ) | languages.multilingual_field_search(
                'medical_center__plural_name', name
            )
            city_query = languages.multilingual_field_search(
                'city__name', name
            )
            owner_query = languages.multilingual_field_search(
                'owner__profile__first_name', name
            ) | languages.multilingual_field_search(
                'owner__profile__last_name', name
            )
            name_query = languages.multilingual_field_search('name', name)
            address_query = languages.multilingual_field_search(
                'address', name
            )
            equipment_query = languages.multilingual_field_search(
                'equipment__name', name
            ) | languages.multilingual_field_search(
                'equipment__description', name
            )
            qs = qs.filter(
                medical_center_query | city_query | owner_query | name_query | address_query | equipment_query
            )
        return qs


EAST = translation.gettext_lazy('East')
WEST = translation.gettext_lazy('West')
NORTH = translation.gettext_lazy('North')
SOUTH = translation.gettext_lazy('South')

REGION_CHOICES = [
    ('E', EAST),
    ('W', WEST),
    ('N', NORTH),
    ('S', SOUTH)
]


class WorkPlace(MultilingualModelMixin, SquareIconMixin, models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.PROTECT, blank=False, null=True,
        verbose_name=translation.gettext_lazy('Medical Center'),
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=False)
    region = models.CharField(
        max_length=1,
        choices=REGION_CHOICES,
        blank=True, null=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=400, blank=False)
    image = models.ImageField(
        upload_to='workplace_images', null=True, blank=True
    )
    notifications = GenericRelation(
        Notification, content_type_field='target_content_type', object_id_field='target_object_id'
    )

    def get_region(self):
        for char, side in REGION_CHOICES:
            if char == self.region:
                return side
        return None

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return self.medical_center.image_url

    @staticmethod
    def get_default_icon():
        return WorkPlaceDefaultIcon.objects.last()

    @property
    def specialists(self):
        employees = [self.owner.profile]
        employments = Membership.objects.filter(
            place=self, status=Membership.ACCEPTED
        )
        for employment in employments:
            employees.append(employment.employee.profile)
        return employees

    def has_staff(self, user):
        return self.owner == user or Membership.objects.filter(
            place=self, employee=user, status=Membership.ACCEPTED
        ).exists()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'address']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    objects = WorkPlaceManager()


class Membership(models.Model):
    WAITING = 'waiting'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (WAITING, WAITING),
        (ACCEPTED, ACCEPTED),
        (REJECTED, REJECTED),
        (CANCELED, CANCELED)
    ]

    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=WAITING
    )

    MEMBERSHIP_REQUEST = 'membership request'
    MEMBERSHIP_ACCEPTED = 'membership accepted'
    MEMBERSHIP_REJECTED = 'membership rejected'
    MEMBERSHIP_CANCELED = 'membership canceled'

    def cancel(self):
        if self.status == self.ACCEPTED:
            self.status = self.CANCELED
            self.save()
            notify.send(
                sender=self.employee, recipient=self.place.owner,
                verb=self.MEMBERSHIP_CANCELED,
                action_object=self, target=self.place, level='info',
            )

    def accept(self):
        if self.status == self.WAITING:
            self.status = self.ACCEPTED
            self.save()
            notify.send(
                sender=self.place.owner, recipient=self.employee,
                verb=self.MEMBERSHIP_ACCEPTED,
                action_object=self, target=self.place, level='success',
            )

    def reject(self):
        if self.status == self.WAITING:
            self.status = self.REJECTED
            self.save()
            notify.send(
                sender=self.place.owner, recipient=self.employee,
                verb=self.MEMBERSHIP_REJECTED, action_object=self,
                target=self.place, level='info'
            )

    def save(self, *args, **kwargs):
        if self.pk:
            created = False
        else:
            created = True
        super().save(*args, **kwargs)
        if created:
            notify.send(
                sender=self.employee, recipient=self.place.owner,
                verb=self.MEMBERSHIP_REQUEST,
                action_object=self, target=self.place, level='info',
            )
