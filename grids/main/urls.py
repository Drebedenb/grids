from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('catalog-category/', catalog_category, name='catalog-category'),
    path('contacts/', contacts, name='contacts'),
    path('product/', product, name='product'),
    path('projects/', projects, name='projects'),
    path('reviews/', reviews, name='reviews'),
]
