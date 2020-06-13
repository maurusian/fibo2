#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    message = "Hello World!"
    return HttpResponse(message)

def fib(request):
    calc = "199393"
    return HttpResponse(calc)
