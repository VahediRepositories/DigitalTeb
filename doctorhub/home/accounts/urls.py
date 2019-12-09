from django.urls import path
from django.views.generic import RedirectView

from . import views
from .phone import urls as phone_urls

urlpatterns = [

    path(
        'send-email/',
        views.email,
        name='send_email',
    ),
    path(
        'accounts/profile/',
        RedirectView.as_view(
            url='/'
        ),
        name='profile'
    ),
    path(
        'accounts/login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'accounts/logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'accounts/signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'accounts/forgot/',
        views.ForgotAccountView.as_view(),
        name='forgot_account'
    ),
    path(
        'accounts/password-change-code/<phone>',
        views.PasswordChangeCodeView.as_view(),
        name='password_change_code'
    ),
    path(
        'accounts/resend-password-change-code/<phone>',
        views.ResendPasswordChangeCodeView.as_view(),
        name='resend_password_change_code'
    ),
    path(
        'accounts/reset-password/<phone>/<code>',
        views.ResetPasswordView.as_view(),
        name='reset_password'
    ),
    path(
        'accounts/invalid-password-change-code/<phone>/<code>',
        views.InvalidPasswordChangeCode.as_view(),
        name='invalid_password_change_code'
    ),
    path(
        'accounts/edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_account'
    ),
    path(
        'accounts/change-password/',
        views.PasswordChangeView.as_view(),
        name='change_password'
    ),


] + phone_urls.urlpatterns
