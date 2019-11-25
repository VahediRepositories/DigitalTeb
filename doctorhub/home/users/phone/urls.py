from django.conf.urls import url
from . import views

urlpatterns = [

    url(
        r'^account/confirmation-code/',
        views.ConfirmationCodeView.as_view(),
        name='confirmation_code'
    ),
    url(
        r'^account/confirmation-code-resend/',
        views.ResendConfirmationCodeView.as_view(),
        name='resend_confirmation_code'
    )

]
