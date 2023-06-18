from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('BuyStock/', views.buy_stock)
]

urlpatterns = format_suffix_patterns(urlpatterns)