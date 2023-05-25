from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:category>-<int:file_number>', product, name='product'),
    path('projects/', projects, name='projects'),
    path('reviews/', reviews, name='reviews'),
    path('compare/', compare, name="compare"),
    path('favorite/', favorite, name="favorite"),
    path('privacy/', privacy, name="privacy"),
    path('акции/', sales, name="sales"),
    path('dostavka/', delivery, name="delivery"),
    path('ustanovka/', installing, name="installing"),
    path('oplata/', paying, name="paying"),
    path('skchema-zakaza/', order_scheme, name="order_scheme"),
    path('garantiya/', guarantee, name="guarantee"),
    path('vopros-otvet/', faq, name="faq"),
]