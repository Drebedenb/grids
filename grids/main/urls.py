from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('контакты/', contacts, name='contacts'),
    path('решетка-на-окно/<int:category>-<int:file_number>', product, name='product'),
    path('наши-работы/', projects, name='projects'),
    path('отзывы-клиентов/', reviews, name='reviews'),
    path('сравнение-решеток-на-окна/', compare, name="compare"),
    path('избранные-решетки-на-окна/', favorite, name="favorite"),
    path('политика-конфиденциальности/', privacy, name="privacy"),
    path('акции/', sales, name="sales"),
    path('sitemap/', sitemap, name="sitemap"),
]