from django.urls import reverse

from .specialties import specialties
from .phones import create_phone
from ..accounts.models import Profile
from ..accounts.phone.models import PasswordChangeCode


def create_profile(user, form):
    profile = Profile.objects.create(
        user=user,
        gender=form.cleaned_data['gender'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
    )
    create_phone(profile, form.cleaned_data['phone'])
    return profile


def verify_password_change_code(phone, code):
    password_change_codes = PasswordChangeCode.objects.filter(
        code=code, used=False
    )
    for password_change_code in password_change_codes:
        if password_change_code.user.profile.phone.number == phone:
            if not password_change_code.is_expired():
                return True
    return False


def use_password_change_code(user, code):
    password_change_codes = PasswordChangeCode.objects.filter(
        user=user, code=code
    )
    for password_change_code in password_change_codes:
        password_change_code.use()


def get_profile_url(user):
    path_name = 'specialist_profile' if specialties.is_specialist(user) else 'profile'
    url = reverse(path_name)
    return url


def get_profile_edit_url(user):
    path_name = 'edit_specialist_account' if specialties.is_specialist(user) else 'edit_account'
    return reverse(path_name)
