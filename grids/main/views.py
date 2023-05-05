import re
import os

from django.db.models import Min, Max
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from urllib.parse import urlencode

# class MockDjangoRedis:
#     def get(self, arg):
#         return None
#
#     def set(arg, bla, ble, blu):
#         return arg


# cache = MockDjangoRedis()

from .models import PriceWinguardMain, PriceWinguardFiles, PriceWinguardSketch

list_of_grids_types = [
    {'title': 'Сварные', 'img_path': 'main/img/grids_types/1_svarnie.webp', 'url': '/сварные-решетки-на-окна'},
    {'title': 'Кованые', 'img_path': 'main/img/grids_types/2_kovanie.webp', 'url': '/кованые-решетки-на-окна-вип-класс'},
    {'title': 'Дутые', 'img_path': 'main/img/grids_types/3_dutie.webp', 'url': '/дутые-решетки-на-окна'},
    {'title': 'Ажурные', 'img_path': 'main/img/grids_types/4_azhurnie.webp', 'url': '/ажурные-решетки-на-окна'},
    {'title': 'Арочные', 'img_path': 'main/img/grids_types/5_arochnie.webp', 'url': '/арочные-решетки-на-окна'},
    {'title': 'Распашные', 'img_path': 'main/img/grids_types/6_raspashnie.webp', 'url': '/распашные-решетки-на-окна'},
    {'title': 'На балкон', 'img_path': 'main/img/grids_types/8_na_lodjiu.webp', 'url': '/решетки-на-балкон'},
    {'title': 'На приямки', 'img_path': 'main/img/grids_types/18_na_pryamki.webp', 'url': '/решетки-на-приямки'},
    {'title': 'На лоджию', 'img_path': 'main/img/grids_types/7_na_balkon.webp', 'url': '/решетки-на-лоджию'},
    {'title': 'Для квартиры', 'img_path': 'main/img/grids_types/9_dlya_kvartiri.webp', 'url': '/решетки-для-квартиры'},
    {'title': 'На первый этаж', 'img_path': 'main/img/grids_types/10_na_perviy.webp', 'url': '/решетки-на-первый-этаж'},
    {'title': 'Цоколь/Подвал', 'img_path': 'main/img/grids_types/11_cokol.webp', 'url': '/решетки-для-цоколя'},
    {'title': 'Для дома', 'img_path': 'main/img/grids_types/12_dlya_doma.webp', 'url': '/решетки-для-дома'},
    {'title': 'Кид-стоп', 'img_path': 'main/img/grids_types/14_ot_vipadenia.webp', 'url': '/решетки-от-выпадения-детей'},
    {'title': 'На кондиционер', 'img_path': 'main/img/grids_types/15_na_condicioner.webp', 'url': '/решетки-на-кондиционер'},
]

list_of_popular_sections = [
    {'title': 'ТОП 100 сварных',  'url': '/топ-100-сварных-решеток-на-окна'},
    {'title': 'ТОП 100 кованых',  'url': '/топ-100-кованых-оконных-решеток'},
    {'title': 'Без открывания',  'url': '/решетки-без-открывания'},
    {'title': 'VIP Класс',  'url': '/кованые-решетки-на-окна-вип-класс'},
]

list_of_kinds = [
    {'title': 'Cварные', 'url': '/сварные-решетки-на-окна'},
    {'title': 'Кованые', 'url': '/кованые-решетки-на-окна-вип-класс'},
    {'title': 'Дутые', 'url': '/дутые-решетки-на-окна'},
    {'title': 'Ажурные', 'url': '/ажурные-решетки-на-окна'},
    {'title': 'Арочные', 'url': '/арочные-решетки-на-окна'},
]

list_of_photos_done = [
    {"name": "photos/1-1/1.webp"},
    {"name": "photos/1-4/1.webp"},
    {"name": "photos/1-16/1.webp"},
    {"name": "photos/1-62/1.webp"},
    {"name": "photos/2-14/1.webp"},
    {"name": "photos/3-16/1.webp"},
    {"name": "photos/3-43/1.webp"},
    {"name": "photos/5-25/1.webp"},
    {"name": "photos/5-59/1.webp"},
    {"name": "photos/6-11/1.webp"},
    {"name": "photos/7-33/1.webp"},
    {"name": "photos/8-17/1.webp"}
]

list_of_photos_done_collapsed = [
    {"name": "photos/2-40/1.webp"},
    {"name": "photos/3-56/1.webp"},
    {"name": "photos/4-4/1.webp"},
    {"name": "photos/4-16/1.webp"},
    {"name": "photos/6-3/1.webp"},
    {"name": "photos/7-34/1.webp"},
    {"name": "photos/8-11/1.webp"},
    {"name": "photos/6-12/1.webp"},
    {"name": "photos/4-48/1.webp"},
    {"name": "photos/5-66/1.webp"},
    {"name": "photos/7-9/1.webp"},
    {"name": "photos/1-67/1.webp"}
]

list_of_reviews = [
    {'id': 'review-1', 'author': 'Иван Семенович Г.', 'author_avatar': 'avatar19.webp', 'project_photo': '1-19/1.webp', 'description': 'Заказ №36378 Решетка на лоджию 3м2. Ответственные люди, я бы так назвал процесс взаимодействия с компанией. Все по плану, без заминок. Главное, что результат хороший и я им доволен.'},
    {'id': 'review-2', 'author': 'Янина Ш.', 'author_avatar': 'avatar25.webp', 'project_photo': '1-4/1.webp', 'description': 'Всем довольна, тамбурную решетчатую дверь мне варили и цветочницу. Прекрасно смотрятся в доме.. мастер позвонил перед выездом на замер. Цена устроила, состояние спустя год очень хорошее'},
    {'id': 'review-3', 'author': 'Иван Б.', 'author_avatar': 'avatar18.webp', 'project_photo': '5-66/1.webp', 'description': 'Заказал решетки ажурные на дачу в стиле кованых ворот. Можно было этого не делать, чуть скинув цену взять прямые. но мне так хотелось. по этому за саму работу мастеров и установщиков ставлю 5, а остальное уже история =В'},
    {'id': 'review-4', 'author': 'Александр В.', 'author_avatar': 'avatar14.webp', 'project_photo': '5-31/1.webp', 'description': 'У меня все хорошо, ребята отлично работают. Знаю их завод под Клином, довольно дешево вышли металлические решетки на подвал и цоколь с установкой. Благодарю!'},
    {'id': 'review-5', 'author': 'Елена Б.', 'author_avatar': 'avatar17.webp', 'project_photo': '6-12/1.webp', 'description': 'Удобно и быстро! Нужны были решетки антикошка и защита от выпадения ребенка, я очень беспокойная мама)) Все супер, особенно общение по телефону и в мессенджерах с мастерами. Так держать, обращусь к вам еще, как куплю дачу'},
    {'id': 'review-6', 'author': 'Кирилл П.', 'author_avatar': 'avatar3.webp', 'project_photo': '1-15/1.webp', 'description': 'Выражаем свою благодарность слаженной работе мастеров ООО «Оконные решётки» за высокое качество изготовления решеток для организации и их установку. Компания обладает профессионализмом и рекомендует себя как надежного подрядчика в вопросе металлических решеток. С уважением, коллектив ХозМастер - Первый.'},
    {'id': 'review-7', 'author': 'Марина Г.', 'author_avatar': 'avatar9.webp', 'project_photo': '1-1/1.webp', 'description': 'Решетки с защитой от детей, от их выпадания мне сделали за 2 дня и привезли домой'},
    {'id': 'review-8', 'author': 'Светлана К.', 'author_avatar': 'avatar24.webp', 'project_photo': '1-3/1.webp', 'description': 'Обратились с запросом решетчатой двери и решеток в магазин. Искали решетки для бизнеса. поставили в срок'},
    {'id': 'review-9', 'author': 'Сергей Н.', 'author_avatar': 'avatar12.webp', 'project_photo': '5-28/1.webp', 'description': 'Как хочется чтобы все в жизни было так же быстро и четко. я НЕ участвовал ни в одном вопросе в моменте производства решеток на окна в дом, ни на моменте их установки. Действительно компания-молодец! Выбрал, заказал, оплатил - привезли'},
    {'id': 'review-10', 'author': 'Лариса Ивановна Л.', 'author_avatar': 'avatar20.webp', 'project_photo': '8-11/1.webp', 'description': 'Раньше сталкивалась с частниками в вопросе стройки- ремонта и боялась столкнуться с ними в выборе оконной решетки на дачу. Совершенно мне этого не хотелось, поэтому сразу искала компанию с опытом, гарантией, договором, точной ценой и без обмана. Также не хотелось долго объяснять все на пальцах по телефону, как обычно с частниками без сайтов происходит.По итогу ни разу не пожалела, что обратилась в вашу компанию. Вы меня прямо спасли от нечестных цен и буквально руководства людьми на объекте. Всем советую, получила идеальную цену/качество'},
    {'id': 'review-11', 'author': 'Галина У.', 'author_avatar': 'avatar7.webp', 'project_photo': '5-41/1.webp', 'description': 'Я далека от строительства, поэтому долго расспрашивала знакомых и искала в интернете информацию про решетки на окна в квартиру. По итогу больше всего мне впечатлили отзывы о фирме “Оконные решетки”, сразу было видно, что они давно на рынке и имеют опыт работы. Я не ошиблась) Привлекло также собственное производство, потому что у меня в апартаментах нестандартного размера окна, а хотелось не тянуть с процессом и поскорее сделать на заказ. Общением с компанией довольна, все рассказали детально, ответили на все мои вопросы, и самое главное, что со мной общались на моем языке без погружения в терминологиюХочу сказать спасибо, сделали все очень качественно, мне не к чему придраться. Нужно было установить решетки на окна 40 на 23 и решетку для кондиционера, все сделали за 3 дня с учетом изготовления.'},
    {'id': 'review-12', 'author': 'Антонина И.', 'author_avatar': 'avatar2.webp', 'project_photo': '1-10/1.webp', 'description': 'Компанию посоветовал коллега для установки решеток на приямки и решетки для бизнеса в целом. У нас офисное здание и искали надежного подрядчика в этой сфере. С уверенностью могу сказать, что компания себя зарекомендовала с отличной стороны. Из перечня работ было изготовление: сварные решетки на окна 30 штук, решетчатые двери внутренние 4 штуки, решетки на кондиционер 5 штук, решетки на приямки 17 штук. '}
]

list_of_reviews_collapsed = [
    {'id': 'review-13', 'author': 'Андрей Алексеевич Б.', 'author_avatar': 'avatar15.webp', 'project_photo': '5-31/1.webp', 'description': 'Заказывал кованые решетки себе на дачу. Очень крепкие, безопасность чувствуется сразу, а главное - красивые, соседи обзавидовались. Быстро и качественно установили, всем советую!'},
    {'id': 'review-14', 'author': 'Алексей Р.', 'author_avatar': 'avatar26.webp', 'project_photo': '5-66/1.webp', 'description': 'Я заказал оконные решетки для моего небольшого антикварного магазина на цокольном этаже. Проблема была в том, что окошки маленькие и не представлял как бы сделать их еще и красивыми. Для меня подготовили эскизы кованых решеток, которые прекрасно вписались в тематику моего магазина. После их установки решил заказать и решетчатые двери на вход. Доволен на 100%! Безопасность и красота одновременно. Большое спасибо за индивидуальный подход'},
    {'id': 'review-15', 'author': 'Нина С.', 'author_avatar': 'avatar30.webp', 'project_photo': '3-16/1.webp', 'description': 'Решили украсить офис, как только началась весна. Заказали цветочницы, но хотели уложиться в свой бюджет. Нам предложили разные опции и смогли подобрать подходящий вариант по цене и по виду. Через пару дней уже приехали установщики, быстро все поставили, даже до обеда успели. Теперь всем коллективом приносим цветочки из дома, окна радуют глаз. Спасибо за оперативность и качество!'},
    {'id': 'review-16', 'author': 'Надежда С.', 'author_avatar': 'avatar23.webp', 'project_photo': '1-82/1.webp', 'description': 'Бесконечно можно смотреть на три вещи: на горящий огонь, на текущую воду и на кованые решетки у меня на даче. Большое спасибо, Вы мастера своего дела!!'},
    {'id': 'review-17', 'author': 'Мария У.', 'author_avatar': 'avatar27.webp', 'project_photo': '1-43/1.webp', 'description': 'На первый этаж квартиры заказала решетки на окна, но хотела что-то более минималистичное, потому что живу в новостройке.Замерщик предложил много вариантов для меня и через три дня уже приехали устанавливать. Просто и со вкусом, как и хотела, спасибо!'},
    {'id': 'review-18', 'author': 'Георгий Р.', 'author_avatar': 'avatar28.webp', 'project_photo': '1-5/1.webp', 'description': 'Замерять приехали в удобное мне время, за это спасибо. Опытные сотрудники, сразу это заметил. Четко и быстро, я доволен.  '},
    {'id': 'review-19', 'author': 'Наталья М.', 'author_avatar': 'avatar32.webp', 'project_photo': '6-25/1.webp', 'description': 'Собрались с мужем лететь в отпуск и нужно было быстро установить решетки на окна из соображений безопасности. С работой справились за пару дней и даже скидку сделали за большой заказ, т.к. дом немаленький. Решетки красивые и надежные, благодарим за срочность выполнения.'},
    {'id': 'review-20', 'author': 'Алексей Сергеевич С..', 'author_avatar': 'avatar33.webp', 'project_photo': '1-143/1.webp', 'description': 'Замерили и установили дутые решетки на окна. Боялся, что может выйти так себе, но получилось очень красиво. Переживал за бюджет, но заказ вышел по карману. Не стыдно рекомендовать, спасибо!'},
    {'id': 'review-21', 'author': 'Андрей Н', 'author_avatar': 'avatar34.webp', 'project_photo': '5-31/1.webp', 'description': 'Фирма очень ответственная. Поставили классические решетки на окна, упор при заказе ставил на прочность. Вышли настолько крепкими, что кажутся крепче самих стен)). Монтаж как по маслу, спасибо Вам.'},
    {'id': 'review-22', 'author': 'Василий Щ', 'author_avatar': 'avatar35.webp', 'project_photo': '5-31/1.webp', 'description': 'Недавно заказал металлические решетки на окна этой компании и остался под впечатлением! Высокое качество и шикарный внешний вид. Всегда поражало то, как умельцы работают с металлом. Спасибо за вам за такую красоту!'},
    {'id': 'review-23', 'author': 'Любовь Г.', 'author_avatar': 'avatar36.webp', 'project_photo': '1-43/1.webp', 'description': 'На прошлой неделе заказала цветочницу для дачи. Крепкая и, как говорится, "на века". Теперь она стала новым украшением нашего дома, а ещё в ней классно смотрятся все цветочные горшки. В общем, превзошли мои ожидания и порадовали ценой.  '},
    {'id': 'review-24', 'author': 'Роман К.', 'author_avatar': 'avatar37.webp', 'project_photo': '1-82/1.webp', 'description': 'У меня есть небольшой продуктовый магазинчик и недавно решил заказать решетчатые двери для склада. Выглядят надежно и кстати пропускают много света, это + к экономии. Сориентировали по выбору и быстро установили. Рекомендую фирму любому владельцу бизнеса, которого интересует и безопасность и внешний вид своего предприятия.'},
    {'id': 'review-25', 'author': 'Екатерина А.', 'author_avatar': 'avatar38.webp', 'project_photo': '1-9/1.webp', 'description': 'Если у вас есть кошки и вы беспокоитесь, что ваши пушистики выпрыгнут за птичками, играя на подоконнике, я рекомендую выбрать решетку антикошку. Ребята быстро ее установили и теперь я спокойна за этих хвостатых охотниц. Мне предложили много вариантов по размерам, отлично все подобрали. Если хотите крепко спать, зная что ваши кошки в безопасности, то заказывайте решетку этой фирмы!'},
    {'id': 'review-26', 'author': 'Даниил Л.', 'author_avatar': 'avatar39.webp', 'project_photo': '1-9/1.webp', 'description': 'Недавно закончил с балконом и хотел решить вопрос безопасности, не портя его внешний вид. Друг посоветовал эту фирму. Вопрос решили за пару дней, решетка выглядит шикарно и самое главное - надежно. Порадовала работа установщиков и сроки выполнения работ. Спасибо!'},
    {'id': 'review-27', 'author': 'Анастасия И.', 'author_avatar': 'avatar40.webp', 'project_photo': '7-34/1.webp', 'description': 'Как директор офиса расположенного в старинном здании, я была обеспокоена как безопасностью, так и внешним видом наших окон. В интернете нашла эту компанию, позвонила и девушки менеджеры завоевали мое сердце. Подобрали специально для нас эскизы и оформили установку. Я в восторге от результата - конструкция не только обеспечивает необходимую нам безопасность, но и прекрасно дополняет архитектурный стиль здания прошлого века. Весь отдел доволен тем, как они выглядят, и мне больше не нужно беспокоиться о безопасности офиса. Спасибо за отлично выполненную работу!'},
    {'id': 'review-28', 'author': 'Иван Ж.', 'author_avatar': 'avatar41.webp', 'project_photo': '1-32/1.webp', 'description': 'Жена любит возиться с цветами, поэтому захотел сделать ей подарок на юбилей. Заказал цветочницы на окна, а на днях их уже установили. Я в этом ничего не понимаю, но по телефону мне помогли с выбором и сделали скидку. Жена безумно рада, теперь вся зелень красуется на окнах. Спасибо вам огромное'},
    {'id': 'review-29', 'author': 'Клим П.', 'author_avatar': 'avatar42.webp', 'project_photo': '1-9/1.webp', 'description': 'Срочно заказывал решетки на подвал. Всё ок, быстро и четко. Даже мышь не пролезет'},
    {'id': 'review-30', 'author': 'Николай Ш.', 'author_avatar': 'avatar43.webp', 'project_photo': '1-54/1.webp', 'description': 'Мы учительским советом решили заказать нашим детям в школу решетчатые двери на спортзал и столовку, потому что уже нет надежды, что старые тоненькие дверки выдержат. Удивило то, что цена совсем не кусается и всё вышло нам по карману. Дети теперь не снесут старые двери толпой, а мы будем спокойны. Большое вам спасибо, всё сделали быстро и профессионально'},

]

list_of_open_types = [
    {"name": "arch", "description": "Арочная", "price": "30", "width": 1000, "height": 1500},
    {"name": "gog", "description": "Глухая-Распашная-Глухая", "price": "1500", "width": 3000, "height": 1500},
    {"name": "o", "description": "Распашная", "price": "1500", "width": 1000, "height": 1500},
    {"name": "oo", "description": "Распашная-Распашная", "price": "2800", "width": 1500, "height": 1500},
]

russian_categories = {
    "металлические-решетки-на-окна": {"title": "", 'url_title': "all", "number_of_category": 'all'},
    "дутые-решетки-на-окна": {"title": "Дутые", 'url_title': "blow", "number_of_category": 'all'}, #TODO: сделать все дутые рещетки а не только одну группу

    "сварные-решетки-на-окна": {"title": "Сварные", 'url_title': "svarka", "number_of_category": 1},
    "арочные-решетки-на-окна": {"title": "Арочные", 'url_title': "svarka", "number_of_category": 'all'},
    "распашные-решетки-на-окна": {"title": "Распашные", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-на-балкон": {"title": "На балкон", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-на-приямки": {"title": "На приямки", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-на-лоджию": {"title": "На лоджию", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-для-квартиры": {"title": "Для квартиры", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-на-первый-этаж": {"title": "На первый этаж", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-для-цоколя": {"title": "Цоколь/Подвал", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-для-дома": {"title": "Для дома", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-от-выпадения-детей": {"title": "Кид-стоп", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-на-кондиционер": {"title": "На кондиционер", 'url_title': "svarka", "number_of_category": 'all'},

    "топ-100-кованых-оконных-решеток": {"title": "Топ-100", 'url_title': "svarka", "number_of_category": 'all'},
    "топ-100-сварных-решеток-на-окна": {"title": "Топ-100", 'url_title': "svarka", "number_of_category": 'all'},
    "решетки-без-открывания": {"title": "Без открывания", 'url_title': "svarka", "number_of_category": 'all'},

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

# one day cache will be stored
TTL_OF_CACHE_SECONDS = 60 * 60 * 24

def get_paginated_url(request, page_number):
    params = request.GET.copy()
    params['page'] = page_number
    return f"{request.path}?{urlencode(params)}"

def get_products_by_category(category_number, min_price, max_price, order_by_name, order_scending, limit):
    products_list_from_cache = cache.get("category_" + str(category_number) + str(min_price) +
                                         str(max_price) + order_by_name + order_scending + str(limit))
    if products_list_from_cache:
        return products_list_from_cache
    dictionary_of_orders = ['price', 'id', 'popularity', 'percent', 'asc', 'desc']
    if order_by_name not in dictionary_of_orders or order_scending not in dictionary_of_orders:
        return []
    if not (isinstance(category_number, int) and isinstance(min_price, int) and isinstance(max_price,
                                                                                           int) and isinstance(limit,
                                                                                                               int)):
        return []

    query = """SELECT *,
                        ROUND(price / (1-percent/100), -1) AS saleprice
                        FROM
                        (SELECT MIN(price_b2c) AS price, ps.id, pf.path, (MOD(ps.id, 3) + 1)*10 + (MOD(ps.id,2) * 5) AS percent,
                        (MOD(ps.id,2) + 4) AS stars_count,
                        {category_number} AS path_folder,
                        ps.number AS path_file
                        FROM price.price_winguard_main pm
                        JOIN price.price_winguard_sketch ps ON pm.price_winguard_sketch_id=ps.id
                        JOIN price.price_winguard_files pf ON pm.price_winguard_sketch_id=pf.price_winguard_sketch_id
                        WHERE category = {category_number}
                        GROUP BY ps.id, pf.path
                        HAVING price > {min_price} AND price < {max_price}
                        ORDER BY {order_by_name} {order_scending}
                        LIMIT {limit}) dup""".format(category_number=category_number, min_price=min_price,
                                                     max_price=max_price
                                                     , order_by_name=order_by_name, order_scending=order_scending,
                                                     limit=limit)
    # subquery = PriceWinguardMain.objects.filter(
    #     price_winguard_sketch__category=category_number,
    #     price_b2c__gt=min_price,
    #     price_b2c__lt=max_price,
    # ).values(
    #     'price_winguard_sketch_id',
    #     'price_winguard_sketch__pricewinguardfiles__path',
    # ).annotate(
    #     price=F('price_b2c'),
    #     percent=(Mod('price_winguard_sketch_id', 3) + 1) * 10 + (Mod('price_winguard_sketch_id', 2) * 5),
    #     path_folder=Value(category_number, output_field=IntegerField()),
    #
    # ).order_by('{order_by_name}'.format(order_by_name=order_by_name))[:limit]
    #
    # query = subquery.annotate(
    #     saleprice=Round(F('price') / (1 - F('percent') / 100), -1),
    # )

    products = PriceWinguardMain.objects.raw(query)
    products_list = []
    for product in products:  # TODO: переписать на ORM
        products_list.append(product)
    cache.set("category_" + str(category_number) + str(min_price) + str(max_price) + order_by_name
              + order_scending + str(limit), products_list, TTL_OF_CACHE_SECONDS)
    return products_list

def get_all_products(min_price, max_price, order_by_name, order_scending, limit):
    products_list_from_cache = cache.get("all_" + str(min_price) +
                                         str(max_price) + order_by_name + order_scending + str(limit))
    if products_list_from_cache:
        return products_list_from_cache
    dictionary_of_orders = ['price', 'id', 'popularity', 'percent', 'asc', 'desc']
    if order_by_name not in dictionary_of_orders or order_scending not in dictionary_of_orders:
        return []
    if not (isinstance(min_price, int) and isinstance(max_price, int) and isinstance(limit, int)):
        return []
    query = """SELECT *,
                        ROUND(price / (1-percent/100), -1) AS saleprice
                        FROM
                        (SELECT MIN(price_b2c) AS price, ps.id, pf.path, (MOD(ps.id, 3) + 1)*10 + (MOD(ps.id,2) * 5) AS percent,
                        (MOD(ps.id,2) + 4) AS stars_count,
                        ps.category AS path_folder,
                        ps.number AS path_file
                        FROM price.price_winguard_main pm
                        JOIN price.price_winguard_sketch ps ON pm.price_winguard_sketch_id=ps.id
                        JOIN price.price_winguard_files pf ON pm.price_winguard_sketch_id=pf.price_winguard_sketch_id
                        GROUP BY ps.id, pf.path
                        HAVING price > {min_price} AND price < {max_price}
                        ORDER BY {order_by_name} {order_scending}
                        LIMIT {limit}) dup""".format(min_price=min_price,
                                                     max_price=max_price
                                                     , order_by_name=order_by_name, order_scending=order_scending,
                                                     limit=limit)
    products = PriceWinguardMain.objects.raw(query)
    products_list = []
    for product in products:  # TODO: переписать на ORM
        products_list.append(product)
    cache.set("all_" + str(min_price) + str(max_price) + order_by_name + order_scending + str(limit),
              products_list, TTL_OF_CACHE_SECONDS)
    return products_list



def get_product_by_sketch_category_and_number(category, number):
    product = cache.get("product_" + str(category) + "_" + str(number))
    if product is None:
        query = """
            SELECT *,
            ROUND(price_b2c / (1-percent/100), -1) AS saleprice
            FROM
            (
            SELECT  ps.category AS path_folder, pm.price_b2c, pm.name, ps.id, 
            (MOD(ps.id, 3) + 1)*10 + (MOD(ps.id,2) * 5) AS percent, 
            (MOD(ps.id,2) + 4) AS stars_count,
            ps.number AS path_file 
            FROM price.price_winguard_main pm
            JOIN price.price_winguard_sketch ps ON pm.price_winguard_sketch_id=ps.id
            JOIN price.price_winguard_files pf ON pm.price_winguard_sketch_id=pf.price_winguard_sketch_id
            WHERE category={category} AND number={number}
            ) inner_query
        """.format(category=category, number=number)
        product = PriceWinguardMain.objects.raw(query)  # TODO: посмотреть что будет при замене на ORM
        product_list = []
        for item in product:
            product_list.append(item)
        cache.set("product_" + str(category) + "_" + str(number), product_list, TTL_OF_CACHE_SECONDS)
        return product_list
    return product


def get_folder_of_photos_by_category_and_number(category, numberOfProduct):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, f'main/static/main/img/projects/{category}/{category}-{numberOfProduct}')


def get_product_project_photos_eight(category, numberOfProduct):
    try:
        img_list = os.listdir(get_folder_of_photos_by_category_and_number(category, numberOfProduct))
    except:
        img_list = []
    for i in range(len(img_list)):
        img_list[i] = f'projects/{category}/{category}-{numberOfProduct}/' + img_list[i]
    for i in range(len(img_list) + 1, 9):
        img_list.append(f'projects/1/1-1/{i}.webp')
    return img_list


def count_products_by_category(category_number):
    count = cache.get("count_" + str(category_number))
    if count is None:
        count = PriceWinguardSketch.objects.filter(category=category_number).count()
        cache.set("count_" + str(category_number), count, TTL_OF_CACHE_SECONDS)
    return count


def get_category_min_price(category_number):
    min_price = cache.get("min_price_" + str(category_number))
    if min_price is None:
        min_price = \
            PriceWinguardMain.objects.filter(price_winguard_sketch__category=category_number).aggregate(
                Min('price_b2c'))[
                'price_b2c__min']
        cache.set("min_price_" + str(category_number), min_price, TTL_OF_CACHE_SECONDS)
    return min_price


def get_category_max_price(category_number):
    max_price = cache.get("max_price_" + str(category_number))
    if max_price is None:
        max_price = PriceWinguardMain.objects.filter(price_winguard_sketch__category=category_number).values(
            'price_winguard_sketch__id') \
            .annotate(min_price=Min('price_b2c')).values('min_price').aggregate(Max('min_price'))['min_price__max']
        cache.set("max_price_" + str(category_number), max_price, TTL_OF_CACHE_SECONDS)
    return max_price


def get_min_price_of_all_products():
    min_price = cache.get("min_price_all")
    if min_price is None:
        min_price = \
            PriceWinguardMain.objects.aggregate(
                Min('price_b2c'))[
                'price_b2c__min']
        cache.set("min_price_all", min_price, TTL_OF_CACHE_SECONDS)
    return min_price

def get_max_price_of_all_products():
    max_price = cache.get("max_price_all")
    if max_price is None:
        max_price = PriceWinguardMain.objects.values(
            'price_winguard_sketch__id') \
            .annotate(min_price=Min('price_b2c')).values('min_price').aggregate(Max('min_price'))['min_price__max']
        cache.set("max_price_all", max_price, TTL_OF_CACHE_SECONDS)
    return max_price

count = {
        "economy": count_products_by_category(1) + count_products_by_category(2),
        "ajur": count_products_by_category(3) + count_products_by_category(4),
        "vip": count_products_by_category(5) + count_products_by_category(6),
        "exlusive": count_products_by_category(7) + count_products_by_category(8),
}
def index(request):
    leaders_of_selling = get_products_by_category(1, 0, 99999, 'id', 'asc', 16)
    min_price_1 = get_category_min_price(1)
    min_price_2 = get_category_min_price(3)
    min_price_3 = get_category_min_price(5)
    min_price_4 = get_category_min_price(7)
    short_list_of_reviews = list_of_reviews[:4]
    short_list_of_reviews_collapsed = list_of_reviews_collapsed[:8]
    context = {
        'title': 'Главная страница',
        'list_of_grids_types': list_of_grids_types,
        'leaders_of_selling': leaders_of_selling,
        'list_of_photos_done': list_of_photos_done,
        'min_price_1': min_price_1,
        'min_price_2': min_price_2,
        'min_price_3': min_price_3,
        'min_price_4': min_price_4,
        'short_list_of_reviews': short_list_of_reviews,
        'short_list_of_reviews_collapsed': short_list_of_reviews_collapsed,
        'count': count
    }
    return render(request, 'main/index.html', context)


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
        max_price_for_sort = 9999999 if request.GET.get('maxPriceByUser') is None else int(
            request.GET.get('maxPriceByUser'))

    if (category["number_of_category"] == 'all'):
        products_list = get_all_products(min_price_for_sort, max_price_for_sort, order_type, order_scending, limit)
        min_price = get_min_price_of_all_products()
        max_price = get_max_price_of_all_products()
    else:
        products_list = get_products_by_category(category["number_of_category"], min_price_for_sort, max_price_for_sort,
                                             order_type, order_scending, limit)
        min_price = get_category_min_price(category["number_of_category"])
        max_price = get_category_max_price(category["number_of_category"])

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 45)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    leaders_of_selling = get_products_by_category(5, min_price_for_sort, max_price_for_sort,
                                                  order_type, order_scending, 15)
    context = {
        'title': 'Каталог металлических решеток',
        'products': products, 'category': category, 'leaders_of_selling': leaders_of_selling,
        'min_price': min_price, 'max_price': max_price, 'list_of_photos_done': list_of_photos_done,
        'list_of_open_types': list_of_open_types,
        'list_of_grids_types': list_of_grids_types,
        'list_of_kinds': list_of_kinds,
        'list_of_popular_sections': list_of_popular_sections,

        'prev_url': get_paginated_url(request, products.previous_page_number()) if products.has_previous() else None, #for pagination
        'next_url': get_paginated_url(request, products.next_page_number()) if products.has_next() else None,

        'count': count
    }
    return render(request, 'main/catalog-category.html', context)


def contacts(request):
    context = {
        'title': 'Контакты',
        'count': count
    }
    return render(request, 'main/contacts.html', context)


price_step_for_category = {
    1: 100,
    2: 100,
    3: 200,
    4: 200,
    5: 1000,
    6: 1000,
    7: 2000,
    8: 2000
}


def product(request, category, file_number):
    product = get_product_by_sketch_category_and_number(category, file_number)
    first_row_product = product[0]
    similar_grids_by_price = get_products_by_category(first_row_product.path_folder,
                                                      first_row_product.price_b2c - price_step_for_category[
                                                          first_row_product.path_folder],
                                                      first_row_product.price_b2c + price_step_for_category[
                                                          first_row_product.path_folder],
                                                      'price', 'asc', 15)
    photos_of_projects = get_product_project_photos_eight(first_row_product.path_folder, first_row_product.path_file)
    context = {
        'title': 'Решетка на окно ' + str(first_row_product.path_folder) + '-' + str(first_row_product.path_file),
        'product': product,
        'list_of_open_types': list_of_open_types,
        'similar_grids_by_price': similar_grids_by_price,
        'photos_of_projects': photos_of_projects,
        'list_of_grids_types': list_of_grids_types,
        'list_of_kinds': list_of_kinds,
        'list_of_popular_sections': list_of_popular_sections,
        'count': count
    }
    return render(request, 'main/product.html', context)


def projects(request):
    context = {
        'title': 'Наши работы',
        'list_of_grids_types': list_of_grids_types,
        'list_of_photos_done': list_of_photos_done,
        'list_of_photos_done_collapsed': list_of_photos_done_collapsed,
        'count': count
    }
    return render(request, 'main/projects.html', context)


def reviews(request):
    context = {
        'title': 'Отзывы клиентов',
        'list_of_reviews': list_of_reviews,
        'list_of_reviews_collapsed': list_of_reviews_collapsed,
        'count': count
    }
    return render(request, 'main/reviews.html', context)


def compare(request):
    str_of_cookies = request.COOKIES.get('Compare')
    if str_of_cookies == '' or str_of_cookies == None:
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
    context = {
        'title': 'Сравнение решеток',
        'products': list_of_compares,
        'count': count
    }
    return render(request, 'main/compare.html', context)


def favorite(request):
    str_of_cookies = request.COOKIES.get('Favorites')
    if str_of_cookies == '':
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
    context = {
        'title': 'Избранные решетки',
        'products': list_of_favorites,
        'count': count
    }
    return render(request, 'main/favorite.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")


def privacy(request):
    context = {
        'title': 'Конфиденциальность',
        'count': count
    }
    return render(request, 'main/privacy.html')
