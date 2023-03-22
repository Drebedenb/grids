from django.http import HttpResponseNotFound
from django.shortcuts import render

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

leaders_of_selling = [
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {}
]


def index(request):
    return render(request, 'main/index.html', {'list_of_grids_types': list_of_grids_types, 'title': 'Главная страница', 'leaders_of_selling': leaders_of_selling})


def catalog(request):
    return render(request, 'main/catalog.html')


def catalog_category(request):
    return render(request, 'main/catalog-category.html')


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
