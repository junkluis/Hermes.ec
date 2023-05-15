from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone


def index(request):
    return HttpResponse("Habla para que yo te conozca.")

def login(request):
    return render(request, 'Zeus/login.html', {})
