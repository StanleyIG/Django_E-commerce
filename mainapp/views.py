from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')  


def about(request):
        return render(request, 'mainapp/about.html')
                