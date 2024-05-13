from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def about(request):
    url = reverse_lazy('mainapp:index')
    return redirect(url)