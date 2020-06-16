#from django.shortcuts import render
from django.http import HttpResponse
from fib.models import FibonacciSums

# Create your views here.
def fib(request,number):
    number = int(number)
    F = FibonacciSums(number)
    #res = '<br>'.join([str(x) for x in F.adjust_result(F.get_fibo_sums())])
    sums = F.get_fibo_sums()
    sums = F.adjust_result(sums)
    #res = F.__repr__('<br>',' + ')
    
    res = '<ul class="list-group">'
    for fibo_sum in sums:
        res+= '<li class="list-group-item">'+' + '.join([str(n) for n in fibo_sum])+'</li>'

    res+= '</ul>'
    
    F.save_to_db()
    return HttpResponse(str(res))


def index(request):
    message = "This app is powered by Fibonacci sequences"
    return HttpResponse(message)


def fib_ask(request):
    message = "<h3>Go to fib/number in the address bar to get all combinations of Fibonacci numbers that add up to number</h3>"
    return HttpResponse(message)

