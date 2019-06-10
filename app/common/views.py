from django.shortcuts import render
from django.http import HttpResponse

from . import services


def index(request):
    return render(request, 'common/index.html')


def version(request):
    v = services.version()
    return HttpResponse(v)
