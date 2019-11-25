from django.core.validators import RegexValidator
from django.db import models
from wagtail.snippets.models import register_snippet
import datetime
from . import configurations


@register_snippet
class Phone(models.Model):
    profile = models.OneToOneField('home.Profile', on_delete=models.CASCADE)
    phone_validator = RegexValidator(
        regex=r'^((\+98)|(0))?\d{10}$'
    )
    number = models.CharField(max_length=20, validators=[phone_validator])
    verified = models.BooleanField(default=False)

    def verify(self):
        self.verified = True
        self.save()

    def __str__(self):
        return str(self.number)


@register_snippet
class ConfirmationCode(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    date = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        diff = self.get_passed_time()
        hours = diff.seconds / 3600
        expired = hours > configurations.CONFIRMATION_CODE_EXPIRATION_HOURS
        print('expired', expired)
        return expired

    def resend_time_passed(self):
        diff = self.get_passed_time()
        seconds = diff.seconds
        return seconds >= configurations.CONFIRMATION_CODE_RESEND_TIME_SECONDS

    def get_remained_resend_time(self):
        diff = self.get_passed_time()
        return configurations.CONFIRMATION_CODE_RESEND_TIME_SECONDS - diff.seconds

    def get_passed_time(self):
        return datetime.datetime.now() - self.date.replace(tzinfo=None)

    def __str__(self):
        return self.code

    class Meta:
        ordering = [
            'date'
        ]
