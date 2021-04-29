from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('minimal_lens_thickness/', views.minimal_lens_thickness, name='minimal_lens_thickness'),
        ]
