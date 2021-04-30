from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return render(request=request, template_name='calculator/index.html')

def minimum_blank_size(request):
    return render(request=request, template_name='calculator/minimum_blank_size.html')
