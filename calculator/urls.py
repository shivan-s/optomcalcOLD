from django.urls import path

from .views import IndexView, MinimumBlankSizeView, MBSCalculate

urlpatterns = [
        path('', IndexView.as_view()),
        path('minimum_blank_size/', MinimumBlankSizeView.as_view()),
        path('mbs_calculate/', MBSCalculate.as_view()),
        ]
