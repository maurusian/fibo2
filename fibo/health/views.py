from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def health_check(request):
    message = "We will conduct a health check for this app"
    return HttpResponse(message)
    
