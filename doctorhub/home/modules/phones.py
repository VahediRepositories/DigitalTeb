from ..authentication.phone.models import Phone


def create_phone(profile, phone_number):
    return Phone.objects.create(
        profile=profile,
        number=phone_number[-10:]
    )
