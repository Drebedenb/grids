from django.urls import path, include

from django.conf.urls.static import static
from grids import settings
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:category_name>', catalog_category, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('product/<slug:sketch_id>', product, name='product'),
    path('projects/', projects, name='projects'),
    path('reviews/', reviews, name='reviews'),
    path('compare/', compare, name="compare"),
    path('favorite/', favorite, name="favorite"),
    path('privacy/', privacy, name="privacy")
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)