from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def catalog(request):
    return render(request,'main/catalog.html')


def catalog_category(request):
    return render(request,'main/catalog-category.html')


def contacts(request):
    return render(request,'main/contacts.html')


def product(request):
    return render(request,'main/product.html')


def projects(request):
    return render(request,'main/projects.html')


def reviews(request):
    return render(request,'main/reviews.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
