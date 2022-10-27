from django.shortcuts import render

# Create your views here.



def display(request):
    context = {

    }
    return render(request, 'foodtruckapp/display.html', context)