from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^(?P<number>\d+)/',views.fib),
    path('',views.fib_ask)
    ]
