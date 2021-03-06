from django.urls import path

from . import views

urlpatterns = [

    path(
        'confirmation-code/',
        views.ConfirmationCodeView.as_view(),
        name='confirmation_code'
    ),
    path(
        'confirmation-code-resend/',
        views.ResendConfirmationCodeView.as_view(),
        name='resend_confirmation_code'
    )

]
