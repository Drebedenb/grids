import re
import traceback

from django.db.models import Min, Max, Count
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import PriceWinguardMain, PriceWinguardFiles, PriceWinguardSketch

list_of_grids_types = [
    {'title': 'Сварные', 'img_path': 'main/img/grids_types/1_svarnie.png'},
    {'title': 'Кованые', 'img_path': 'main/img/grids_types/2_kovanie.png'},
    {'title': 'Дутые', 'img_path': 'main/img/grids_types/3_dutie.png'},
    {'title': 'Ажурные', 'img_path': 'main/img/grids_types/4_azhurnie.png'},
    {'title': 'Арочные', 'img_path': 'main/img/grids_types/5_arochnie.png'},
    {'title': 'Распашные', 'img_path': 'main/img/grids_types/6_raspashnie.png'},
    {'title': 'На балкон', 'img_path': 'main/img/grids_types/7_na_balkon.png'},
    {'title': 'На приямки', 'img_path': 'main/img/grids_types/18_na_pryamki.png'},
    {'title': 'На лоджию', 'img_path': 'main/img/grids_types/8_na_lodjiu.png'},
    {'title': 'Для квартиры', 'img_path': 'main/img/grids_types/9_dlya_kvartiri.png'},
    {'title': 'На первый этаж', 'img_path': 'main/img/grids_types/10_na_perviy.png'},
    {'title': 'Цоколь/Подвал', 'img_path': 'main/img/grids_types/11_cokol.png'},
    {'title': 'Для дома', 'img_path': 'main/img/grids_types/12_dlya_doma.png'},
    {'title': 'Антикошка', 'img_path': 'main/img/grids_types/13_antikoshka.png'},
    {'title': 'От выпадения детей', 'img_path': 'main/img/grids_types/14_ot_vipadenia.png'},
    {'title': 'На кондиционер', 'img_path': 'main/img/grids_types/15_na_condicioner.png'},
    {'title': 'Под цветы', 'img_path': 'main/img/grids_types/16_pod_cveti.png'},
    {'title': 'В подъезд', 'img_path': 'main/img/grids_types/17_v_podezd.png'},
]

list_of_photos_done = [
    {"name": "photo74.png"},
    {"name": "photo75.png"},
    {"name": "photo76.png"},
    {"name": "photo77.png"},
    {"name": "photo78.png"},
    {"name": "photo79.png"},
    {"name": "photo80.png"},
    {"name": "photo81.png"},
    {"name": "photo82.png"},
    {"name": "photo83.png"},
    {"name": "photo84.png"},
    {"name": "photo85.png"}
]

list_of_open_types = [
    {"name": "arch", "description": "Арочная", "price": "30", "width": 1000, "height": 1500},
    {"name": "gog", "description": "Глухая-Распашная-Глухая", "price": "1500", "width": 3000, "height": 1500},
    {"name": "o", "description": "Распашная", "price": "1500", "width": 1000, "height": 1500},
    {"name": "oo", "description": "Распашная-Распашная", "price": "2800", "width": 1500, "height": 1500},
]

russian_categories = {
    "все": {"title": "Все", 'url_title': "all", "number_of_category": 1},
    "решетки-на-окна-эконом-класс": {"title": "Эконом", 'url_title': "svarka", "number_of_category": 1},
    "дутые-решетки-на-окна-эконом-класс": {"title": "Дутые Эконом", 'url_title': "svarka_dut", "number_of_category": 2},
    "ажурные-решетки-на-окна": {"title": "Ажурные", 'url_title': "ajur", "number_of_category": 3},
    "дутые-ажурные-решетки": {"title": "Дутые Ажурные", 'url_title': "ajur_dut", "number_of_category": 4},
    "кованые-решетки-на-окна-вип-класс": {"title": "VIP", 'url_title': "kovka", "number_of_category": 5},
    "кованые-дутые-решетки-вип-класса": {"title": "Дутые VIP", 'url_title': "kovka_dut", "number_of_category": 6},
    "эксклюзивные-кованые-решетки": {"title": "Эксклюзив", 'url_title': "vip", "number_of_category": 7},
    "дутые-эксклюзивные-решетки": {"title": "Дутые Эксклюзив", 'url_title': "vip_dut", "number_of_category": 8},
}

# def get_products_amount_by_category(category_number)

arr_of_sale = [15, 10, 20, 30, 25, 20, 10, 20, 20, 30, 25, 10, 10, 20, 30, 10, 20, 30, 15, 10]


def get_products_by_category(category_number, min_price, max_price, order_by_name, order_scending, limit):
    dictionary_of_orders = ['price', 'id', 'popularity', 'asc', 'desc']
    if order_by_name not in dictionary_of_orders or order_scending not in dictionary_of_orders:

        return []
    if not (isinstance(category_number, int) and isinstance(min_price, int) and isinstance(max_price, int) and isinstance(limit, int)):
        return []
    query = """SELECT MIN(price_b2c) AS price, ps.id, pf.path
                FROM price.price_winguard_main pm
                JOIN price.price_winguard_sketch ps ON pm.price_winguard_sketch_id=ps.id 
                JOIN price.price_winguard_files pf ON pm.price_winguard_sketch_id=pf.price_winguard_sketch_id
                WHERE category = {category_number}
                GROUP BY ps.id, pf.path
                HAVING price > {min_price} AND price < {max_price}
                ORDER BY {order_by_name} {order_scending}
                LIMIT {limit}""".format(category_number=category_number, min_price=min_price, max_price=max_price
                                          ,order_by_name=order_by_name,order_scending=order_scending,limit=limit)
    products = PriceWinguardMain.objects.raw(query)
    for product in products:
        path_arr = "".join(re.findall("\/\d+\/\d+", product.path)).split("/")
        product.path_folder = path_arr[1]
        product.path_file = path_arr[2]
        product.percent = arr_of_sale[product.id % 20]
        product.saleprice = int((product.price / (1 - product.percent / 100))/10) * 10 #TODO: реализовать через SQL
    return products


def count_products_by_category(category_number):
    return PriceWinguardSketch.objects.filter(category=category_number).count()


def get_category_min_price(category_number):
    min_price = \
        PriceWinguardMain.objects.filter(price_winguard_sketch__category=category_number).aggregate(Min('price_b2c'))[
            'price_b2c__min']
    return min_price


def get_category_max_price(category_number):
    max_price = \
        PriceWinguardMain.objects.filter(price_winguard_sketch__category=category_number).aggregate(Max('price_b2c'))[
            'price_b2c__max']
    products = PriceWinguardMain.objects.filter(price_winguard_sketch__category=category_number)
    for product in products:
        print(product)
    return max_price

def index(request):
    count = {
        "economy": count_products_by_category(1),
        "ajur": count_products_by_category(3),
        "vip": count_products_by_category(5),
        "exlusive": count_products_by_category(7),
    }
    leaders_of_selling = get_products_by_category(1, 0, 99999, 'id', 'asc', 9999)
    min_price_1 = get_category_min_price(1)
    min_price_2 = get_category_min_price(3)
    min_price_3 = get_category_min_price(5)
    min_price_4 = get_category_min_price(7)
    return render(request, 'main/index.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Главная страница',
                                               'leaders_of_selling': leaders_of_selling,
                                               'list_of_photos_done': list_of_photos_done,
                                               'min_price_1': min_price_1,
                                               'min_price_2': min_price_2,
                                               'min_price_3': min_price_3,
                                               'min_price_4': min_price_4,
                                               'count': count
                                               })


def catalog_category(request, category_name):
    if category_name not in russian_categories:
        return HttpResponseNotFound("Page NOT found")
    category = russian_categories[category_name]
    min_price_for_sort = 0
    max_price_for_sort = 9999999
    order_type = 'id'
    order_scending = 'asc'
    limit = 9999
    if request.method == 'GET':
        order_type = 'id' if request.GET.get('order') is None else request.GET.get('order')
        order_scending = 'asc' if request.GET.get('orderScending') is None else request.GET.get('orderScending')
        min_price_for_sort = 0 if request.GET.get('minPriceByUser') is None else int(request.GET.get('minPriceByUser'))
        max_price_for_sort = 9999999 if request.GET.get('maxPriceByUser') is None else int(request.GET.get('maxPriceByUser'))
    products_list = get_products_by_category(category["number_of_category"], min_price_for_sort, max_price_for_sort, order_type, order_scending, limit)

    min_price = get_category_min_price(category["number_of_category"])
    max_price = get_category_max_price(category["number_of_category"])

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    leaders_of_selling = []
    return render(request, 'main/catalog-category.html',
                  {'title': 'Каталог', 'list_of_grids_types': list_of_grids_types,
                   'products': products, 'category': category, 'leaders_of_selling': leaders_of_selling,
                   'min_price': min_price, 'max_price': max_price, 'list_of_photos_done': list_of_photos_done,
                   'list_of_open_types': list_of_open_types})


def contacts(request):
    return render(request, 'main/contacts.html')


def product(request, sketch_id):
    product = {}
    path = "".join(
        re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=sketch_id).path))
    path_arr = path.split("/")
    product["path_folder"] = path_arr[1]
    product["path_file"] = path_arr[2]
    product['additional_info'] = list(
        PriceWinguardMain.objects.filter(price_winguard_sketch_id=sketch_id).values('price_b2c', 'name'))
    return render(request, 'main/product.html', {'product': product, 'list_of_open_types': list_of_open_types})


def projects(request):
    return render(request, 'main/projects.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Каталог',
                                                  'list_of_photos_done': list_of_photos_done})


def reviews(request):
    return render(request, 'main/reviews.html')


def compare(request):
    str_of_cookies = request.COOKIES.get('Compare')
    if str_of_cookies is '':
        return render(request, 'main/compare.html',
                      {'products': []})
    list_of_compares_cookie = str_of_cookies.split(',')
    list_of_compares = []
    for sketch_id in list_of_compares_cookie:
        product = {"id": sketch_id}
        product["price"] = \
            PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c')[0]['price_b2c']
        product["percent"] = arr_of_sale[int(product["id"]) % 20]
        product["saleprice"] = int(product["price"] * (1 + product["percent"] / 100))
        path = "".join(
            re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
        path_arr = path.split("/")
        product["path_folder"] = path_arr[1]
        product["path_file"] = path_arr[2]
        product['additional_info'] = list(
            PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c', 'name'))
        list_of_compares.append(product)
    return render(request, 'main/compare.html',
                  {'products': list_of_compares})


def favorite(request):
    str_of_cookies = request.COOKIES.get('Favorites')
    if str_of_cookies is '':
        return render(request, 'main/favorite.html',
                      {'products': []})
    list_of_favorites_cookie = str_of_cookies.split(',')
    list_of_favorites = []
    for sketch_id in list_of_favorites_cookie:
        product = {"id": sketch_id}
        product["price"] = \
        PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c')[0]['price_b2c']
        product["percent"] = arr_of_sale[int(product["id"]) % 20]
        product["saleprice"] = int(product["price"] * (1 + product["percent"] / 100))
        path = "".join(
            re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
        path_arr = path.split("/")
        product["path_folder"] = path_arr[1]
        product["path_file"] = path_arr[2]
        list_of_favorites.append(product)
    return render(request, 'main/favorite.html', {'products': list_of_favorites})


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
