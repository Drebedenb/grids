from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('kontakty/', contacts, name='contacts'),
    path('reshetka-na-okno/<int:category>-<int:file_number>', product, name='product'),
    path('nashi-raboty/', projects, name='projects'),
    path('otzyvy-klientov/', reviews, name='reviews'),
    path('sravnenie-reshetki-na-okna/', compare, name="compare"),
    path('lyubimye-reshetki-na-okna/', favorite, name="favorite"),
    path('privacy/', privacy, name="privacy"),
    path('akcii/', sales, name="sales")
]