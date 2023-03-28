import os
import urllib.request
from ftplib import FTP
import json
from django.core.exceptions import ImproperlyConfigured

from django.http import HttpResponseNotFound
from django.shortcuts import render

from grids.settings import BASE_DIR
from .models import PriceWinguardMain, PriceWinguardFiles, PriceWinguardSketch

list_of_grids_types = [
    {'title': 'Сварные', 'img_path': 'main/img/grids_types/icons1.png'},
    {'title': 'Кованые', 'img_path': 'main/img/grids_types/icons10.png'},
    {'title': 'Дутые', 'img_path': 'main/img/grids_types/icons11.png'},
    {'title': 'Ажурные', 'img_path': 'main/img/grids_types/icons12.png'},
    {'title': 'Арочные', 'img_path': 'main/img/grids_types/icons13.png'},
    {'title': 'Распашные', 'img_path': 'main/img/grids_types/icons14.png'},
    {'title': 'На балкон', 'img_path': 'main/img/grids_types/icons15.png'},
    {'title': 'На приямки', 'img_path': 'main/img/grids_types/icons16.png'},
    {'title': 'На лоджию', 'img_path': 'main/img/grids_types/icons17.png'},
    {'title': 'Для квартиры', 'img_path': 'main/img/grids_types/icons18.png'},
    {'title': 'На первый этаж', 'img_path': 'main/img/grids_types/icons19.png'},
    {'title': 'Цоколь/Подвал', 'img_path': 'main/img/grids_types/icons20.png'},
    {'title': 'Для дома', 'img_path': 'main/img/grids_types/icons21.png'},
    {'title': 'Антикошка', 'img_path': 'main/img/grids_types/icons22.png'},
    {'title': 'От выпадания детей', 'img_path': 'main/img/grids_types/icons23.png'},
    {'title': 'На кондиционер', 'img_path': 'main/img/grids_types/icons24.png'},
    {'title': 'Под цветы', 'img_path': 'main/img/grids_types/icons25.png'},
    {'title': 'В подъезд', 'img_path': 'main/img/grids_types/icons25.png'},
]

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# ftp = FTP()
# ftp.set_debuglevel(2)
# ftp.connect(get_secret("FTP_URL"))
# ftp.login(get_secret("DB_USERNAME"), get_secret("DB_PASSWORD"))
# ftp.dir()
# ftp.close()


def index(request):
    products = PriceWinguardMain.objects.all()[:50]
    # for product in products:
    #     file = PriceWinguardFiles.objects.get(price_winguard_sketch_id=product.price_winguard_sketch_id)
    #     product.path = file.path
    #     data = urllib.request.urlretrieve("ftp://92.63.107.238/winguard/sketch/1/3/catalog.jpg")
    return render(request, 'main/index.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Главная страница',
                                               'leaders_of_selling': products})


def catalog(request):
    return render(request, 'main/catalog.html')


categories = {  # there are categories and their number in database. It depends on database structure what number is
    "svarka": {"title": "Сварные", "number_of_category": 1},
    "svarka-dutaya": {"title": "Дутые сварные", "number_of_category": 2},
    "ajur": {"title": "Ажурные", "number_of_category": 3},
    "ajur-dutaya": {"title": "Дутые ажурные", "number_of_category": 4},
    "kovka": {"title": "Кованные", "number_of_category": 5},
    "kovka-dutaya": {"title": "Дутые кованные", "number_of_category": 6},
    "vip": {"title": "VIP", "number_of_category": 7},
    "vip-dutaya": {"title": "Дутые VIP", "number_of_category": 8},
}


def catalog_category(request, category_name):
    if category_name not in categories:
        return HttpResponseNotFound("Page NOT found")
    category = categories[category_name]
    products = PriceWinguardSketch.objects.filter(category=category["number_of_category"]).values('category','id')
    return render(request, 'main/catalog-category.html', {'title': 'Каталог',
                                                          'products': products, 'category': category})


def contacts(request):
    return render(request, 'main/contacts.html')


def product(request):
    return render(request, 'main/product.html')


def projects(request):
    return render(request, 'main/projects.html')


def reviews(request):
    return render(request, 'main/reviews.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
