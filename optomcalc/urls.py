from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('optomcalc_settings/', admin.site.urls),
    path('', include('calculator.urls')),
]
