from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('minimum_blank_size/', views.minimum_blank_size, name='minimum_blank_size'),
        ]
