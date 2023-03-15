from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
