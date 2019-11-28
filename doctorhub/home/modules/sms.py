import json
import random

import requests
from django.conf import settings
from requests.exceptions import ConnectionError

from ..accounts.phone.models import *


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
        return None
    except KeyError as e:
        return None


def send_confirmation_code(phone):
    return send_code(
        phone, "VerificationCode", "16641", save_confirmation_code
    )


def send_password_change_code(phone):
    return send_code(
        phone, "PasswordChangeCode", "17723", save_password_change_code
    )


def resend_confirmation_code(user):
    confirmation_code = get_last_confirmation_code(user)
    if (not confirmation_code) or confirmation_code.resend_time_passed():
        send_confirmation_code(user.profile.phone)
        return True
    return False


def resend_password_change_code(phone):
    user = Phone.get_user_by_phone_number(phone)
    password_change_code = get_last_password_change_code(user)
    if (not password_change_code) or password_change_code.resend_time_passed():
        send_password_change_code(user.profile.phone)
        return True
    return False


def verify_phone(user, code):
    confirmation_codes = ConfirmationCode.objects.filter(code=code)
    for confirmation_code in confirmation_codes:
        if confirmation_code.phone.profile.user == user:
            if not confirmation_code.is_expired():
                confirmation_code.phone.verify()
                return True
    return False


def get_remained_confirmation_resend_time(user):
    confirmation_code = get_last_confirmation_code(user)
    return get_remained_resend_time(confirmation_code)


def get_remained_password_change_resend_time(phone):
    user = Phone.get_user_by_phone_number(phone)
    password_change_code = get_last_password_change_code(user)
    return get_remained_resend_time(password_change_code)


def get_remained_resend_time(code):
    if not code:
        return CODE_RESEND_TIME_SECONDS
    else:
        return code.get_remained_resend_time()


def get_last_confirmation_code(user):
    return ConfirmationCode.objects.filter(phone=user.profile.phone).last()


def get_last_password_change_code(user):
    return PasswordChangeCode.objects.filter(user=user).last()


def send_code(phone, parameter_name, template_id, save_to_database):
    if settings.SILENCED_SMS:
        return True
    confirmation_code = create_confirmation_code()
    confirmation_code = str(confirmation_code)
    url = 'https://RestfulSms.com/api/UltraFastSend'
    data = {
        "ParameterArray": [
            {
                "Parameter": parameter_name,
                "ParameterValue": confirmation_code,
            }
        ],
        "Mobile": phone.number,
        "TemplateId": template_id,
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
            save_to_database(phone, confirmation_code)
            return True
        except ConnectionError as e:
            return False


def save_confirmation_code(phone, confirmation_code):
    ConfirmationCode.objects.create(
        phone=phone, code=confirmation_code
    )


def save_password_change_code(phone, confirmation_code):
    PasswordChangeCode.objects.create(
        user=phone.profile.user, code=confirmation_code
    )


def create_confirmation_code():
    return random.randint(
        10 ** (CODE_LENGTH - 1),
        (10 ** CODE_LENGTH) - 1
    )
