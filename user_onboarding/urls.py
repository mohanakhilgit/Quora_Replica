from django.urls import path

from .views import signup_user, login_user, logout_user


urlpatterns = [
    path('signup/', signup_user, name='signup_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]