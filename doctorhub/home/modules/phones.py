from ..accounts.phone.models import Phone


def create_phone(profile, phone_number):
    return Phone.objects.create(
        profile=profile,
        number=phone_number
    )


def phone_exists(phone_number):
    return Phone.objects.filter(
        number=phone_number
    ).exists()


def verified_phone_exists(phone_number):
    return Phone.objects.filter(
        number=phone_number, verified=True
    ).exists()
