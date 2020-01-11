from django.urls import path, include
from django.views.generic import RedirectView

from . import views
from .phone import urls as phone_urls

urlpatterns = [

    path(
        'profile/',
        RedirectView.as_view(
            url='/'
        ),
        name='profile'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'forgot/',
        views.ForgotAccountView.as_view(),
        name='forgot_account'
    ),
    path(
        'password-change-code/<phone>',
        views.PasswordChangeCodeView.as_view(),
        name='password_change_code'
    ),
    path(
        'resend-password-change-code/<phone>',
        views.ResendPasswordChangeCodeView.as_view(),
        name='resend_password_change_code'
    ),
    path(
        'reset-password/<phone>/<code>',
        views.ResetPasswordView.as_view(),
        name='reset_password'
    ),
    path(
        'invalid-password-change-code/<phone>/<code>',
        views.InvalidPasswordChangeCode.as_view(),
        name='invalid_password_change_code'
    ),
    path(
        'edit/',
        views.UserProfileUpdateView.as_view(),
        name='edit_account'
    ),
    path(
        'change-password/',
        views.PasswordChangeView.as_view(),
        name='change_password'
    ),
    path(
        'phones/',
        include(phone_urls)
    )

]
