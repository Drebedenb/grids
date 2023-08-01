from django.urls import path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('sitemap.xml', TemplateView.as_view(template_name='main/sitemap/sitemap.xml', content_type='application/xml'),
         name='sitemap'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="main/robots.txt", content_type="text/plain"),
    ),
    # path('handle-post-request/', handle_post_request, name='handle_post_request'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('контакты/', contacts, name='contacts'),
    path('решетка-на-окно/<int:category>-<int:file_number>', product, name='product'),
    path('наши-работы/', projects, name='projects'),
    path('отзывы-клиентов/', reviews, name='reviews'),
    path('сравнение-решеток-на-окна/', compare, name="compare"),
    path('избранные-решетки-на-окна/', favorite, name="favorite"),
    path('политика-конфиденциальности/', privacy, name="privacy"),
    path('акции/', sales, name="sales"),
    path('dostavka/', delivery, name="delivery"),
    path('ustanovka/', installing, name="installing"),
    path('oplata/', paying, name="paying"),
    path('garantiya/', guarantee, name="guarantee"),
    path('vopros-otvet/', faq, name="faq"),
    path('o-kompanii/', about, name="about"),
    path('pokraska/', color, name="pokraska"),
    path('skchema-zakaza/', order_scheme, name="order_scheme"),
    path('thanks/', thanks, name="thanks"),
]

handler404 = page_not_found
