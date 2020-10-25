from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "quotes/index.html")


def login(request):
    return HttpResponse("sparta")


def register(request):
    return HttpResponse("Register")
