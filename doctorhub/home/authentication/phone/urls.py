from django.conf.urls import url
from . import views

urlpatterns = [

    url(
        r'^accounts/confirmation-code/',
        views.ConfirmationCodeView.as_view(),
        name='confirmation_code'
    ),
    url(
        r'^accounts/confirmation-code-resend/',
        views.ResendConfirmationCodeView.as_view(),
        name='resend_confirmation_code'
    )

]
