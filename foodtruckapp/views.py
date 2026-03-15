from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.

def display(request):
    context = {}
    return render(request, 'foodtruckapp/display.html', context)

def controller(request):
    context = {}
    return render(request, 'foodtruckapp/controller.html', context)

def whereami(request):
    url = "https://www.google.com/maps/dir/?api=1"
    return HttpResponseRedirect(url)
