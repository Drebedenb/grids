import re
from django.db.models import Min, Max
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
    {"name": "arch", "description": "Арочная", "price": "30"},
    {"name": "gog", "description": "Глухая-Распашная-Глухая", "price": "1500"},
    {"name": "o", "description": "Распашная", "price": "1500"},
    {"name": "og", "description": "Распашная-Глухая", "price": "1500"},
    {"name": "ogo", "description": "Распашная-Глухая-Распашная", "price": "3000"},
    {"name": "oo", "description": "Распашная-Распашная", "price": "2800"},
    {"name": "solid", "description": "Глухая", "price": "0"}
]

categories = {  # there are categories and their number in database. It depends on database structure what number is
    "svarka": {"title": "Сварные",'url_title': "svarka" , "number_of_category": 1},
    "svarka_dut": {"title": "Дутые сварные",'url_title': "svarka_dut" , "number_of_category": 2},
    "ajur": {"title": "Ажурные",'url_title': "ajur" , "number_of_category": 3},
    "ajur_dut": {"title": "Дутые ажурные",'url_title': "ajur_dut" , "number_of_category": 4},
    "kovka": {"title": "Кованые",'url_title': "kovka" , "number_of_category": 5},
    "kovka_dut": {"title": "Дутые кованые",'url_title': "kovka_dut" , "number_of_category": 6},
    "vip": {"title": "VIP",'url_title': "vip" , "number_of_category": 7},
    "vip_dut": {"title": "Дутые VIP",'url_title': "vip_dut" , "number_of_category": 8},
}

russian_categories = {
    "все": {"title": "Все", 'url_title': "all" , "number_of_category": 1},
    "решетки-на-окна-эконом-класс": {"title": "Эконом",'url_title': "svarka" , "number_of_category": 1},
    "дутые-решетки-на-окна-эконом-класс": {"title": "Дутые Эконом",'url_title': "svarka_dut" , "number_of_category": 2},
    "ажурные-решетки-на-окна": {"title": "Ажурные",'url_title': "ajur" , "number_of_category": 3},
    "дутые-ажурные-решетки": {"title": "Дутые Ажурные",'url_title': "ajur_dut" , "number_of_category": 4},
    "кованые-решетки-на-окна-вип-класс": {"title": "VIP",'url_title': "kovka" , "number_of_category": 5},
    "кованые-дутые-решетки-вип-класса": {"title": "Дутые VIP",'url_title': "kovka_dut" , "number_of_category": 6},
    "эксклюзивные-кованые-решетки": {"title": "Эксклюзив",'url_title': "vip" , "number_of_category": 7},
    "дутые-эксклюзивные-решетки": {"title": "Дутые Эксклюзив",'url_title': "vip_dut" , "number_of_category": 8},
}


# def get_products_amount_by_category(category_number)

def get_products_by_category(category_number):
    products = PriceWinguardSketch.objects.filter(category=category_number) \
                   .values('id').annotate(min_pricewinguardmain=Min('pricewinguardmain')).values('min_pricewinguardmain', 'id')
    for product in products:
        try:
            path = "".join(
                re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
            path_arr = path.split("/")
            product["path_folder"] = path_arr[1]
            product["path_file"] = path_arr[2]
            try:
                additional_info = PriceWinguardMain.objects.get(id=product["min_pricewinguardmain"])
                product["price"] = additional_info.price_b2c
                product["width"] = additional_info.name
            except:
                product["price"] = "Нет данных в БД"
                product["width"] = "Нет данных в БД"
        except:
            product["price"] = "Нет данных в БД"
            product["path_folder"] = 1
            product["path_file"] = 1
    return products


def index(request):
    products = get_products_by_category(1)
    return render(request, 'main/index.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Главная страница',
                                               'leaders_of_selling': products})

def catalog_category(request, category_name):
    if category_name not in russian_categories:
        return HttpResponseNotFound("Page NOT found")

    category = russian_categories[category_name]
    products_list = get_products_by_category(category["number_of_category"])

    min_price = products_list[0]["price"]
    max_price = products_list[0]["price"]
    try:
        for product in products_list:
            if min_price > product["price"]:
                min_price = product["price"]
            if max_price < product["price"]:
                max_price = product["price"]
    except:
        min_price=min_price

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # leaders_of_selling = get_products_by_category(5)
    leaders_of_selling = [];
    return render(request, 'main/catalog-category.html', {'title': 'Каталог','list_of_grids_types': list_of_grids_types,
                                                          'products': products, 'category': category, 'leaders_of_selling': leaders_of_selling,
                                                          'min_price': min_price, 'max_price': max_price})


def contacts(request):
    return render(request, 'main/contacts.html')


def product(request, product_name):
    sketch_id = re.findall("\d+", product_name)[2]
    product = {}
    path = "".join(
        re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=sketch_id).path))
    path_arr = path.split("/")
    product["path_folder"] = path_arr[1]
    product["path_file"] = path_arr[2]
    product['additional_info'] = list(PriceWinguardMain.objects.filter(price_winguard_sketch_id=sketch_id).values('price_b2c', 'name'))
    return render(request, 'main/product.html',{'product': product, 'list_of_open_types': list_of_open_types})


def projects(request):
    return render(request, 'main/projects.html',{'list_of_grids_types': list_of_grids_types, 'title': 'Каталог', 'list_of_photos_done': list_of_photos_done})


def reviews(request):
    return render(request, 'main/reviews.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
