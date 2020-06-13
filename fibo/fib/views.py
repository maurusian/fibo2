#from django.shortcuts import render
from django.http import HttpResponse
from fib.models import FibonacciSums

# Create your views here.
def fib(request,number):
    number = int(number)

    F = FibonacciSums(number)
    res = '<br>'.join([str(x) for x in F.adjust_result(F.get_fibo_sums())])
    
    return HttpResponse(str(res))

def index(request):
    message = "Adnymics test task 2"
    return HttpResponse(message)
