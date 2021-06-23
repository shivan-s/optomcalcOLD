from django.urls import path

from .views import IndexView, MinimumBlankSizeView, MBSCalculate

urlpatterns = [
        path('', IndexView.as_view(), name='index'),
        path('minimum_blank_size/', MinimumBlankSizeView.as_view(), name='minimum_blank_size'),
        path('mbs_calculate/', MBSCalculate.as_view()),
        ]
