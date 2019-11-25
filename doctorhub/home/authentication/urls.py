from django.conf.urls import url
from . import views as auth_views

urlpatterns = [

    url(
        r'^accounts/login/',
        auth_views.LoginView.as_view(),
        name='login'
    ),
    url(
        r'^accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^accounts/signup/',
        auth_views.SignUpView.as_view(),
        name='signup'
    ),

]
