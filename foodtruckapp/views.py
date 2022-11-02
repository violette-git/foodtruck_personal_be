from urllib import request
from django.shortcuts import render
# import lxml.html.usedoctest
from django.template import engines
from django.http import HttpResponse, HttpResponseRedirect



import lxml.html
import requests
import html

# Create your views here.



def display(request):
    context = {

    }
    return render(request, 'foodtruckapp/display.html', context)

def controller(request):

    context = {

    }

    return render(request, 'foodtruckapp/controller.html', context)

def whereami(request):
	# if request.method == 'GET':
		
	url = "https://www.google.com/maps/dir/?api=1"
	payload = ""
	headers = {
	}
	
	# url2 = "https://www.google.com/recaptcha/api/siteverify"


	response = requests.request("GET", url, headers=headers, data=payload)
	# print(response.text)
	html = response.text
	# print(html)
	django_engine = engines['django']
	template = django_engine.from_string(html)
	# test = lxml.html.fromstring(f'{html}')
	# print(template.render(), 'templates', '----------------------------------------------')
	new_template = template.render()
	context = {
		'stuff': new_template
	}
	# template.render(context)
	# return render(request, 'foodtruckapp/whereami.html', context)
	return HttpResponseRedirect(url)