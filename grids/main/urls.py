from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('<str:page_name>/', render_page),  # page_name is the name of the page and file
]
