from django.urls import path, include
from . import views


app_name = 'foodtruckapp'

urlpatterns = [
    path('display/', views.display, name='display')

] 