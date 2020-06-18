#from django.shortcuts import render
from django.http import HttpResponse
from fib.models import FibonacciSums, RequestResponse
import time

# Create your views here.
def fib(request,number):
    start = time.time()
    
    req_path = request.path_info

    rr = RequestResponse.get_object_by_request_path(request_path = req_path)

    if rr is not None:
        total = time.time() - start
        res = 'Elapsed time: '+"{:.2f}".format(total)+' second<br><br>'+rr.response_html
        return HttpResponse(res)
    else:
        number = int(number)
        F = FibonacciSums(number)
        #res = '<br>'.join([str(x) for x in F.adjust_result(F.get_fibo_sums())])
        sums = F.get_fibo_sums2()
        sums = F.remove_duplicates()
        #test = FibonacciSums(5).get_fibo_sums2()
        #sums = F.adjust_result(sums)
        #res = F.__repr__('<br>',' + ')
        
        res = '<ul class="list-group">'
        for fibo_sum in sums:
            #res+= '<li class="list-group-item">'+' + '.join([str(n) for n in fibo_sum])+'</li>'
            res+= '<li class="list-group-item">'+str(fibo_sum)+'</li>'

        res+= '</ul>'
        
        F.save_to_db()
        rr = RequestResponse.get_object_by_request_path(request_path = req_path)
        if rr is None:
            RequestResponse(request_path = req_path, response_html = res).save()
        total = time.time() - start
        
        res = 'Elapsed time: '+"{:.2f}".format(total)+' second<br><br>'+res #+'<br><br>'+str(test)
        
        return HttpResponse(str(res))


def index(request):
    message = "This app is powered by Fibonacci sequences"
    return HttpResponse(message)


def fib_ask(request):
    message = "<h3>Go to fib/number in the address bar to get all combinations of Fibonacci numbers that add up to number</h3>"
    return HttpResponse(message)

