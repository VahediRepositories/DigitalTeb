from django.urls import reverse

from ..accounts.models import Profile
from .phones import create_phone


def create_profile(user, form):
    profile = Profile.objects.create(
        user=user,
        gender=form.cleaned_data['gender'],
        birthdate=form.cleaned_data['birthdate'],
    )
    create_phone(profile, form.cleaned_data['phone'])
    return profile


def get_logout_url():
    return reverse('logout')


def get_login_url():
    return reverse('login')


def get_signup_url():
    return reverse('signup')
