from django.shortcuts import render

# Create your views here.



def display(request):
    context = {

    }
    return render(request, 'foodtruckapp/display.html', context)

def controller(request):

    context = {

    }

    return render(request, 'foodtruckapp/controller.html', context)