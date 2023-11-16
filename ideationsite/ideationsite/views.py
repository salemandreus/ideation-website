from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html",{"title":"Welcome"})

def about(request):
    return render(request, "about.html",{"title":"About Us"})

def contact(request):
    return render(request, "contact.html",{"title":"Contact Us"})
