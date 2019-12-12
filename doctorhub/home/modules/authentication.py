from .phones import create_phone
from ..accounts.models import Profile
from ..accounts.phone.models import PasswordChangeCode


def create_profile(user, form):
    profile = Profile.objects.create(
        user=user,
        gender=form.cleaned_data['gender'],
        # birthdate=form.cleaned_data['birthdate'],
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
