from PIL import Image
from django.contrib.auth.models import User
from django.utils import translation
from django.db import models
from django.db.models import DateField
from django.contrib.staticfiles.templatetags.staticfiles import static
from wagtail.snippets.models import register_snippet

MALE = 'M'
FEMALE = 'F'
NOT_BINARY = 'N'

GENDER_CHOICES = [
    (
        NOT_BINARY,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'None of them'
        )
    ),
    (
        FEMALE,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'Female'
        )
    ),
    (
        MALE,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'Male'
        )
    ),
]

AVATARS = 'doctorhub/more/images/avatars/'
MALE_AVATAR = AVATARS + 'male.png'
FEMALE_AVATAR = AVATARS + 'female.png'
NONE_AVATAR = AVATARS + 'none.png'


@register_snippet
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    profile_image = models.ImageField(
        upload_to='profile_pics', null=True, blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=NOT_BINARY,
    )
    birthdate = DateField(blank=False)

    @property
    def image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            if self.gender == MALE:
                return static(MALE_AVATAR)
            elif self.gender == FEMALE:
                return static(FEMALE_AVATAR)
            else:
                return static(NONE_AVATAR)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    def make_square_image(self):
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height != img.width:
                size = min(img.height, img.width)
                img = img.resize((size, size))
                img.save(self.profile_image.path)

    def compress_image(self):
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 512 or img.width > 512:
                output_size = (512, 512)
                img = img.resize(output_size)
                img.save(self.profile_image.path)

    def __str__(self):
        return self.user.username
