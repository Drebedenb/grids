from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('product/<slug:sketch_id>', product, name='product'),
    path('projects/', projects, name='projects'),
    path('reviews/', reviews, name='reviews'),
    path('compare/', compare, name="compare"),
    path('favorite/', favorite, name="favorite")
]