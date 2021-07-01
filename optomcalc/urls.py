from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('optomcalc_settings/', admin.site.urls),
    path('', include('calculator.urls')),
]
