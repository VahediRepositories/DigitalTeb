from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import get_object_or_404
from wagtail.snippets.models import register_snippet

import datetime


CODE_LENGTH = 6
CODE_EXPIRATION_HOURS = 10
CODE_RESEND_TIME_SECONDS = 300


@register_snippet
class Phone(models.Model):
    profile = models.OneToOneField('home.Profile', on_delete=models.CASCADE)
    phone_validator = RegexValidator(
        regex=r'^\d{10}$'
    )
    number = models.CharField(
        max_length=20,
        validators=[phone_validator],
        unique=True,
    )
    verified = models.BooleanField(default=False)

    def verify(self):
        self.verified = True
        self.save()

    def __str__(self):
        return str(self.number)

    @staticmethod
    def get_user_by_phone_number(phone_number):
        phone = get_object_or_404(Phone, number=phone_number)
        return phone.profile.user


class Code(models.Model):
    code = models.CharField(max_length=CODE_LENGTH)
    date = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        diff = self.get_passed_time()
        hours = diff.seconds / 3600
        return hours > CODE_EXPIRATION_HOURS

    def resend_time_passed(self):
        diff = self.get_passed_time()
        seconds = diff.seconds
        return seconds >= CODE_RESEND_TIME_SECONDS

    def get_remained_resend_time(self):
        diff = self.get_passed_time()
        return CODE_RESEND_TIME_SECONDS - diff.seconds

    def get_passed_time(self):
        return datetime.datetime.now() - self.date.replace(tzinfo=None)

    class Meta:
        abstract = True
        ordering = [
            'date'
        ]


@register_snippet
class ConfirmationCode(Code):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


@register_snippet
class PasswordChangeCode(Code):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def use(self):
        self.used = True
        self.save()

    def __str__(self):
        return self.code

