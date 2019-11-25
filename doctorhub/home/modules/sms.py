import json
import random

import requests
from django.conf import settings
from requests.exceptions import ConnectionError

from ..users.phone.models import *
from ..users.phone import configurations


def get_token_key():
    url = 'https://RestfulSms.com/api/Token'
    data = {
        'UserApiKey': settings.SMS_API_KEY,
        'SecretKey': settings.SMS_SECRET_KEY,
    }
    data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            url=url, data=data, headers=headers
        )
        response = response.json()
        token_key = response['TokenKey']
        return token_key
    except ConnectionError as e:
        print(str(e))
        print()
        return None
    except KeyError as e:
        print(str(e))
        print()
        return None


def send_confirmation_sms(phone):
    confirmation_code = create_confirmation_code()
    confirmation_code = str(confirmation_code)
    url = 'https://RestfulSms.com/api/UltraFastSend'
    data = {
        "ParameterArray": [
            {
                "Parameter": "VerificationCode",
                "ParameterValue": confirmation_code,
            }
        ],
        "Mobile": phone.number,
        "TemplateId": "16641"
    }
    data = json.dumps(data)
    token_key = get_token_key()
    if token_key:
        try:
            headers = {
                "x-sms-ir-secure-token": token_key,
                "Content-Type": "application/json",
            }
            requests.post(
                url=url,
                data=data,
                headers=headers
            )
            ConfirmationCode.objects.create(
                phone=phone, code=confirmation_code
            )
            return True
        except ConnectionError as e:
            print(str(e))
            print()
            return False


def create_confirmation_code():
    return random.randint(
        10 ** (configurations.CONFIRMATION_CODE_LENGTH - 1),
        (10 ** configurations.CONFIRMATION_CODE_LENGTH) - 1
    )


def verify_phone(user, code):
    confirmation_codes = ConfirmationCode.objects.filter(code=code)
    for confirmation_code in confirmation_codes:
        if confirmation_code.phone.profile.user == user:
            if not confirmation_code.is_expired():
                confirmation_code.phone.verify()
                return True
    return False


def resend_code(user):
    confirmation_code = get_last_confirmation_code(user)
    if not confirmation_code:
        send_confirmation_sms(user.profile.phone)
        return True
    elif confirmation_code.resend_time_passed():
        send_confirmation_sms(user.profile.phone)
        return True
    return False


def get_remained_resend_time(user):
    confirmation_code = get_last_confirmation_code(user)
    if not confirmation_code:
        return configurations.CONFIRMATION_CODE_RESEND_TIME_SECONDS
    else:
        return confirmation_code.get_remained_resend_time()


def get_last_confirmation_code(user):
    return ConfirmationCode.objects.filter(phone=user.profile.phone).last()
