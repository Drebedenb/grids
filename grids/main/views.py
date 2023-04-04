import re
from django.db.models import Min
from django.http import HttpResponseNotFound
from django.shortcuts import render

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

categories = {  # there are categories and their number in database. It depends on database structure what number is
    "all": {"title": "Все", 'url_title': "all" , "number_of_category": 1},
    "svarka": {"title": "Сварные",'url_title': "svarka" , "number_of_category": 1},
    "svarka_dut": {"title": "Дутые сварные",'url_title': "svarka_dut" , "number_of_category": 2},
    "ajur": {"title": "Ажурные",'url_title': "ajur" , "number_of_category": 3},
    "ajur_dut": {"title": "Дутые ажурные",'url_title': "ajur_dut" , "number_of_category": 4},
    "kovka": {"title": "Кованые",'url_title': "kovka" , "number_of_category": 5},
    "kovka_dut": {"title": "Дутые кованые",'url_title': "kovka_dut" , "number_of_category": 6},
    "vip": {"title": "VIP",'url_title': "vip" , "number_of_category": 7},
    "vip_dut": {"title": "Дутые VIP",'url_title': "vip_dut" , "number_of_category": 8},
}


def get_products_by_category(category_number):
    products = PriceWinguardSketch.objects.filter(category=category_number) \
                   .values('id').annotate(min_pricewinguardmain=Min('pricewinguardmain')).values('min_pricewinguardmain', 'id')[:12]
                   # .values('id', 'pricewinguardfiles').annotate(min_pricewinguardmain=Min('pricewinguardmain')).order_by('category', 'id', 'pricewinguardfiles')[:20]
    for product in products:
        path = "".join(re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
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
    return products


def index(request):
    products = get_products_by_category(1)
    return render(request, 'main/index.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Главная страница',
                                               'leaders_of_selling': products})


def catalog_category(request, category_name):
    if category_name not in categories:
        return HttpResponseNotFound("Page NOT found")
    category = categories[category_name]
    products = get_products_by_category(category["number_of_category"])
    # leaders_of_selling = get_products_by_category(5)
    leaders_of_selling = [];
    return render(request, 'main/catalog-category.html', {'title': 'Каталог',
                                                          'products': products, 'category': category, 'leaders_of_selling': leaders_of_selling})


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
    print(product)
    return render(request, 'main/product.html', product)


def projects(request):
    return render(request, 'main/projects.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Каталог'})


def reviews(request):
    return render(request, 'main/reviews.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")
