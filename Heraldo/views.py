from django.http import HttpResponse


def index(request):
    return HttpResponse("La más dulce vida consiste en no saber nada.")