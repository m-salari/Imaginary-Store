from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user)
]


urlpatterns = format_suffix_patterns(urlpatterns)