from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView, SystemConfigView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('config', SystemConfigView.as_view(), name='config')
]
