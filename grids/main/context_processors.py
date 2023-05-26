list_of_grids_purpose = [
    {'title': 'На балкон', 'img_path': 'main/img/grids_types/7_na_balkon.webp', 'url': '/решетки-на-балкон'},
    {'title': 'На приямки', 'img_path': 'main/img/grids_types/18_na_pryamki.webp', 'url': '/решетки-на-приямки'},
    {'title': 'На лоджию', 'img_path': 'main/img/grids_types/8_na_lodjiu.webp', 'url': '/решетки-на-лоджию'},
    {'title': 'Для квартиры', 'img_path': 'main/img/grids_types/9_dlya_kvartiri.webp', 'url': '/решетки-для-квартиры'},
    {'title': 'На первый этаж', 'img_path': 'main/img/grids_types/10_na_perviy.webp', 'url': '/решетки-на-первый-этаж'},
    {'title': 'Цоколь/Подвал', 'img_path': 'main/img/grids_types/11_cokol.webp', 'url': '/решетки-для-цоколя'},
    {'title': 'Для дома', 'img_path': 'main/img/grids_types/12_dlya_doma.webp', 'url': '/решетки-для-дома'},
    {'title': 'Кид-стоп', 'img_path': 'main/img/grids_types/14_ot_vipadenia.webp','url': '/решетки-от-выпадения-детей'},
    {'title': 'На кондиционер', 'img_path': 'main/img/grids_types/15_na_condicioner.webp','url': '/решетки-на-кондиционер'},
    {'title': 'Внутренние', 'img_path': 'main/img/grids_types/12_dlya_doma.webp', 'url': '/внутренние-решетки'},
    {'title': 'Для дачи', 'img_path': 'main/img/grids_types/8_na_lodjiu.webp', 'url': '/решетки-для-дачи'},
]

list_of_categories = [
    {'title': 'Эконом', 'url': '/дутые-и-обычные-решетки-на-окна-эконом-класс'},
    {'title': 'Ажурные', 'url': '/дутые-и-обычные-ажурные-решетки'},
    {'title': 'VIP', 'url': '/дутые-и-обычные-решетки-вип-класса'},
    {'title': 'Эксклюзив', 'url': '/дутые-и-обычные-эксклюзивные-решетки'},
]

list_of_classes = [
    {'title': 'Дутые', 'url': '/дутые-решетки-на-окна'},
    {'title': 'Обычные', 'url': '/решетки-на-окна-без-дутости'}
]

list_of_open_types = [
    {'title': 'Арочная', 'url': '/арочные-решетки-на-окна'},
    {'title': 'Распашные', 'url': '/распашные-решетки-на-окна'},
    {'title': 'Без открывания', 'url': '/решетки-без-открывания'},
]

list_of_kinds = [
    {'title': 'Cварные', 'url': '/сварные-решетки-на-окна'},
    {'title': 'Кованые', 'url': '/кованые-решетки-на-окна'},
]

list_of_popular_sections = [
    {'title': 'ТОП 100 сварных', 'url': '/топ-100-сварных-решеток-на-окна'},
    {'title': 'ТОП 100 кованых', 'url': '/топ-100-кованых-оконных-решеток'},
]

list_of_dropdown_sections_for_clients = [
    {'title': 'Доставка', 'url': '/dostavka/'},
    {'title': 'Установка', 'url': '/ustanovka/'},
    {'title': 'Оплата', 'url': '/oplata/'},
    # {'title': 'Схема заказа', 'url': '/skchema-zakaza/'},
    {'title': 'Гарантия', 'url': '/garantiya/'},
    # {'title': 'Вопрос-ответ', 'url': '/vopros-otvet/'},
]
def grids_purpose_categories_classes_openTypes_kinds_popularSections(request):
    return {'list_of_grids_purpose': list_of_grids_purpose,
            'list_of_categories': list_of_categories,
            'list_of_classes': list_of_classes,
            'list_of_open_types': list_of_open_types,
            'list_of_kinds': list_of_kinds,
            'list_of_popular_sections': list_of_popular_sections,
            'list_of_dropdown_sections_for_clients': list_of_dropdown_sections_for_clients
            }