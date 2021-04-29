from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return render(request=request, template_name='calculator/index.html')

def minimal_lens_thickness(request):
    return render(request=request, template_name='calculator/minimum_lens_thickness.html')
