import re
import os
import requests
import json

from django.shortcuts import redirect
from django.db.models import Min, Max, F
from django.db.models.functions import Round
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from urllib.parse import urlencode
from .models import PriceWinguardMain, PriceWinguardFiles, PriceWinguardSketch

class MockDjangoRedis:
    def get(self, arg):
        return None

    def set(arg, bla, ble, blu):
        return arg
cache = MockDjangoRedis()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_dir = os.path.join(base_dir, 'main/static/main/img/')

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
    {'id': 'review-1', 'author': 'Иван', 'author_avatar': 'avatar19.webp', 'project_photo': '1-19/1.webp',
     'description': 'Заказ №36378 Решетка на лоджию 3м2. Ответственные люди, я бы так назвал процесс взаимодействия с компанией. Все по плану, без заминок. Главное, что результат хороший и я им доволен.'},
    {'id': 'review-2', 'author': 'Янина Ш.', 'author_avatar': 'avatar25.webp', 'project_photo': '1-4/1.webp',
     'description': 'Всем довольна, тамбурную решетчатую дверь мне варили и цветочницу. Прекрасно смотрятся в доме.. мастер позвонил перед выездом на замер. Цена устроила, состояние спустя год очень хорошее'},
    {'id': 'review-3', 'author': 'Иван Б.', 'author_avatar': 'avatar18.webp', 'project_photo': '5-66/1.webp',
     'description': 'Заказал решетки ажурные на дачу в стиле кованых ворот. Можно было этого не делать, чуть скинув цену взять прямые. но мне так хотелось. по этому за саму работу мастеров и установщиков ставлю 5, а остальное уже история =В'},
    {'id': 'review-4', 'author': 'Александр В.', 'author_avatar': 'avatar14.webp', 'project_photo': '5-31/1.webp',
     'description': 'У меня все хорошо, ребята отлично работают. Знаю их завод под Клином, довольно дешево вышли металлические решетки на подвал и цоколь с установкой. Благодарю!'},
    {'id': 'review-5', 'author': 'Елена Б.', 'author_avatar': 'avatar17.webp', 'project_photo': '6-12/1.webp',
     'description': 'Удобно и быстро! Нужны были решетки антикошка и защита от выпадения ребенка, я очень беспокойная мама)) Все супер, особенно общение по телефону и в мессенджерах с мастерами. Так держать, обращусь к вам еще, как куплю дачу'},
    {'id': 'review-6', 'author': 'Кирилл П.', 'author_avatar': 'avatar3.webp', 'project_photo': '1-15/1.webp',
     'description': 'Выражаем свою благодарность слаженной работе мастеров ООО «Оконные решётки» за высокое качество изготовления решеток для организации и их установку. Компания обладает профессионализмом и рекомендует себя как надежного подрядчика в вопросе металлических решеток. С уважением, коллектив ХозМастер - Первый.'},
    {'id': 'review-7', 'author': 'Марина Г.', 'author_avatar': 'avatar9.webp', 'project_photo': '1-1/1.webp',
     'description': 'Решетки с защитой от детей, от их выпадания мне сделали за 2 дня и привезли домой'},
    {'id': 'review-8', 'author': 'Светлана К.', 'author_avatar': 'avatar24.webp', 'project_photo': '1-3/1.webp',
     'description': 'Обратились с запросом решетчатой двери и решеток в магазин. Искали решетки для бизнеса. поставили в срок'},
    {'id': 'review-9', 'author': 'Сергей Н.', 'author_avatar': 'avatar12.webp', 'project_photo': '5-28/1.webp',
     'description': 'Как хочется чтобы все в жизни было так же быстро и четко. я НЕ участвовал ни в одном вопросе в моменте производства решеток на окна в дом, ни на моменте их установки. Действительно компания-молодец! Выбрал, заказал, оплатил - привезли'},
    {'id': 'review-18', 'author': 'Георгий Р.', 'author_avatar': 'avatar28.webp', 'project_photo': '1-5/1.webp',
     'description': 'Замерять приехали в удобное мне время, за это спасибо. Опытные сотрудники, сразу это заметил. Четко и быстро, я доволен.  '},
    {'id': 'review-13', 'author': 'Андрей Б.', 'author_avatar': 'avatar15.webp',
     'project_photo': '5-31/1.webp',
     'description': 'Заказывал кованые решетки себе на дачу. Очень крепкие, безопасность чувствуется сразу, а главное - красивые, соседи обзавидовались. Быстро и качественно установили, всем советую!'},
    {'id': 'review-16', 'author': 'Надежда С.', 'author_avatar': 'avatar23.webp', 'project_photo': '1-82/1.webp',
     'description': 'Бесконечно можно смотреть на три вещи: на горящий огонь, на текущую воду и на кованые решетки у меня на даче. Большое спасибо, Вы мастера своего дела!!'},
]

list_of_reviews_collapsed = [
    {'id': 'review-11', 'author': 'Галина У.', 'author_avatar': 'avatar7.webp', 'project_photo': '5-39/1.webp',
     'description': 'Я далека от строительства, поэтому долго расспрашивала знакомых и искала в интернете информацию про решетки на окна в квартиру. По итогу больше всего мне впечатлили отзывы о фирме “Оконные решетки”, сразу было видно, что они давно на рынке и имеют опыт работы. Я не ошиблась) Привлекло также собственное производство, потому что у меня в апартаментах нестандартного размера окна, а хотелось не тянуть с процессом и поскорее сделать на заказ. Общением с компанией довольна, все рассказали детально, ответили на все мои вопросы, и самое главное, что со мной общались на моем языке без погружения в терминологиюХочу сказать спасибо, сделали все очень качественно, мне не к чему придраться. Нужно было установить решетки на окна 40 на 23 и решетку для кондиционера, все сделали за 3 дня с учетом изготовления.'},
    {'id': 'review-14', 'author': 'Алексей Р.', 'author_avatar': 'avatar26.webp', 'project_photo': '5-66/1.webp',
     'description': 'Я заказал оконные решетки для моего небольшого антикварного магазина на цокольном этаже. Проблема была в том, что окошки маленькие и не представлял как бы сделать их еще и красивыми. Для меня подготовили эскизы кованых решеток, которые прекрасно вписались в тематику моего магазина. После их установки решил заказать и решетчатые двери на вход. Доволен на 100%! Безопасность и красота одновременно. Большое спасибо за индивидуальный подход'},
    {'id': 'review-15', 'author': 'Нина С.', 'author_avatar': 'avatar30.webp', 'project_photo': '3-16/1.webp',
     'description': 'Решили украсить офис, как только началась весна. Заказали цветочницы, но хотели уложиться в свой бюджет. Нам предложили разные опции и смогли подобрать подходящий вариант по цене и по виду. Через пару дней уже приехали установщики, быстро все поставили, даже до обеда успели. Теперь всем коллективом приносим цветочки из дома, окна радуют глаз. Спасибо за оперативность и качество!'},
    {'id': 'review-12', 'author': 'Антонина И.', 'author_avatar': 'avatar2.webp', 'project_photo': '1-10/1.webp',
     'description': 'Компанию посоветовал коллега для установки решеток на приямки и решетки для бизнеса в целом. У нас офисное здание и искали надежного подрядчика в этой сфере. С уверенностью могу сказать, что компания себя зарекомендовала с отличной стороны. Из перечня работ было изготовление: сварные решетки на окна 30 штук, решетчатые двери внутренние 4 штуки, решетки на кондиционер 5 штук, решетки на приямки 17 штук. '},
    {'id': 'review-17', 'author': 'Мария У.', 'author_avatar': 'avatar27.webp', 'project_photo': '1-43/1.webp',
     'description': 'На первый этаж квартиры заказала решетки на окна, но хотела что-то более минималистичное, потому что живу в новостройке.Замерщик предложил много вариантов для меня и через три дня уже приехали устанавливать. Просто и со вкусом, как и хотела, спасибо!'},
    {'id': 'review-10', 'author': 'Лариса', 'author_avatar': 'avatar20.webp', 'project_photo': '8-11/1.webp',
     'description': 'Раньше сталкивалась с частниками в вопросе стройки- ремонта и боялась столкнуться с ними в выборе оконной решетки на дачу. Совершенно мне этого не хотелось, поэтому сразу искала компанию с опытом, гарантией, договором, точной ценой и без обмана. Также не хотелось долго объяснять все на пальцах по телефону, как обычно с частниками без сайтов происходит.По итогу ни разу не пожалела, что обратилась в вашу компанию. Вы меня прямо спасли от нечестных цен и буквально руководства людьми на объекте. Всем советую, получила идеальную цену/качество'},
    {'id': 'review-19', 'author': 'Наталья М.', 'author_avatar': 'avatar32.webp', 'project_photo': '6-25/1.webp',
     'description': 'Собрались с мужем лететь в отпуск и нужно было быстро установить решетки на окна из соображений безопасности. С работой справились за пару дней и даже скидку сделали за большой заказ, т.к. дом немаленький. Решетки красивые и надежные, благодарим за срочность выполнения.'},
    {'id': 'review-20', 'author': 'Алексей Сергеевич С..', 'author_avatar': 'avatar33.webp',
     'project_photo': '1-143/1.webp',
     'description': 'Замерили и установили дутые решетки на окна. Боялся, что может выйти так себе, но получилось очень красиво. Переживал за бюджет, но заказ вышел по карману. Не стыдно рекомендовать, спасибо!'},
    {'id': 'review-21', 'author': 'Андрей Н', 'author_avatar': 'avatar34.webp', 'project_photo': '5-31/1.webp',
     'description': 'Фирма очень ответственная. Поставили классические решетки на окна, упор при заказе ставил на прочность. Вышли настолько крепкими, что кажутся крепче самих стен)). Монтаж как по маслу, спасибо Вам.'},
    {'id': 'review-22', 'author': 'Василий Щ', 'author_avatar': 'avatar35.webp', 'project_photo': '5-31/1.webp',
     'description': 'Недавно заказал металлические решетки на окна этой компании и остался под впечатлением! Высокое качество и шикарный внешний вид. Всегда поражало то, как умельцы работают с металлом. Спасибо за вам за такую красоту!'},
    {'id': 'review-23', 'author': 'Любовь Г.', 'author_avatar': 'avatar36.webp', 'project_photo': '1-43/1.webp',
     'description': 'На прошлой неделе заказала цветочницу для дачи. Крепкая и, как говорится, "на века". Теперь она стала новым украшением нашего дома, а ещё в ней классно смотрятся все цветочные горшки. В общем, превзошли мои ожидания и порадовали ценой.  '},
    {'id': 'review-24', 'author': 'Роман К.', 'author_avatar': 'avatar37.webp', 'project_photo': '1-82/1.webp',
     'description': 'У меня есть небольшой продуктовый магазинчик и недавно решил заказать решетчатые двери для склада. Выглядят надежно и кстати пропускают много света, это + к экономии. Сориентировали по выбору и быстро установили. Рекомендую фирму любому владельцу бизнеса, которого интересует и безопасность и внешний вид своего предприятия.'},
    {'id': 'review-25', 'author': 'Екатерина А.', 'author_avatar': 'avatar38.webp', 'project_photo': '1-9/1.webp',
     'description': 'Если у вас есть кошки и вы беспокоитесь, что ваши пушистики выпрыгнут за птичками, играя на подоконнике, я рекомендую выбрать решетку антикошку. Ребята быстро ее установили и теперь я спокойна за этих хвостатых охотниц. Мне предложили много вариантов по размерам, отлично все подобрали. Если хотите крепко спать, зная что ваши кошки в безопасности, то заказывайте решетку этой фирмы!'},
    {'id': 'review-26', 'author': 'Даниил Л.', 'author_avatar': 'avatar39.webp', 'project_photo': '1-9/1.webp',
     'description': 'Недавно закончил с балконом и хотел решить вопрос безопасности, не портя его внешний вид. Друг посоветовал эту фирму. Вопрос решили за пару дней, решетка выглядит шикарно и самое главное - надежно. Порадовала работа установщиков и сроки выполнения работ. Спасибо!'},
    {'id': 'review-27', 'author': 'Анастасия И.', 'author_avatar': 'avatar40.webp', 'project_photo': '7-34/1.webp',
     'description': 'Как директор офиса расположенного в старинном здании, я была обеспокоена как безопасностью, так и внешним видом наших окон. В интернете нашла эту компанию, позвонила и девушки менеджеры завоевали мое сердце. Подобрали специально для нас эскизы и оформили установку. Я в восторге от результата - конструкция не только обеспечивает необходимую нам безопасность, но и прекрасно дополняет архитектурный стиль здания прошлого века. Весь отдел доволен тем, как они выглядят, и мне больше не нужно беспокоиться о безопасности офиса. Спасибо за отлично выполненную работу!'},
    {'id': 'review-28', 'author': 'Иван Ж.', 'author_avatar': 'avatar41.webp', 'project_photo': '1-32/1.webp',
     'description': 'Жена любит возиться с цветами, поэтому захотел сделать ей подарок на юбилей. Заказал цветочницы на окна, а на днях их уже установили. Я в этом ничего не понимаю, но по телефону мне помогли с выбором и сделали скидку. Жена безумно рада, теперь вся зелень красуется на окнах. Спасибо вам огромное'},
    {'id': 'review-29', 'author': 'Клим П.', 'author_avatar': 'avatar42.webp', 'project_photo': '1-9/1.webp',
     'description': 'Срочно заказывал решетки на подвал. Всё ок, быстро и четко. Даже мышь не пролезет'},
    {'id': 'review-30', 'author': 'Николай Ш.', 'author_avatar': 'avatar43.webp', 'project_photo': '1-54/1.webp',
     'description': 'Мы учительским советом решили заказать нашим детям в школу решетчатые двери на спортзал и столовку, потому что уже нет надежды, что старые тоненькие дверки выдержат. Удивило то, что цена совсем не кусается и всё вышло нам по карману. Дети теперь не снесут старые двери толпой, а мы будем спокойны. Большое вам спасибо, всё сделали быстро и профессионально'},

]

list_of_open_types_for_calculator = [
    {"name": "arch", "description": "Арочная", "price": "30"},
    {"name": "gog", "description": "Глухая-Распашная-Глухая", "price": "1500"},
    {"name": "o", "description": "Распашная", "price": "1500"},
    {"name": "oo", "description": "Распашная-Распашная", "price": "2800"},
]

list_of_sales_items = [
    {'image_path': 'main/img/sale_baners/sale_baner2.webp', 'description': 'Закажите бесплатный вызов замерщика и оплатите заказ в тот же день, чтобы получить скидку в 10%'},
    {'image_path': 'main/img/sale_baners/sale_baner.webp', 'description': 'Получите скидку в 20% при 100% предоплате ( для физических лиц )'},
    {'image_path': 'main/img/sale_baners/sale_baner3.webp', 'description': 'Создадим проект на основе Ваших эскизов и размеров, если Вы не найдете подходящий макет в нашем каталоге'},
    {'image_path': 'main/img/sale_baners/sale_baner4.webp', 'description': 'При заказе от 3-х решеток за каждую дополнительную единицу Вы получаете скидку 1%. Максимальная скидка - 10%.'},
    {'image_path': 'main/img/sale_baners/sale_baner6.webp', 'description': 'Закажите бесплатные замер и консультацию. Наши сотрудники свяжутся с Вами для уточнения деталей и направят к Вам мастера для проведения технического рассчета'},
    {'image_path': 'main/img/sale_baners/sale_baner5.webp', 'description': 'Заказывая у нас решетки на окна, Вы получаете максимально выгодную цену. Мы уверены в этом и готовы предоставить скидку, если Вы найдете такой же товар дешевле!'},
]

list_of_deliveries = [
    {'name': 'Балашиха ', 'price': '600'},
    {'name': 'Бронницы ', 'price': '1600'},
    {'name': 'Волоколамский район', 'price': '1100'},
    {'name': 'Воскресенский район', 'price': '2100'},
    {'name': 'Дзержинский', 'price': '600'},
    {'name': 'Дмитровский район', 'price': '900'},
    {'name': 'Долгопрудный', 'price': '600'},
    {'name': 'Домодедово', 'price': '1600'},
    {'name': 'Дубна', 'price': '1000'},
    {'name': 'Егорьевский район', 'price': '2500'},
    {'name': 'Железнодорожный', 'price': '800'},
    {'name': 'Жуковский', 'price': '1200'},
    {'name': 'Зарайский район', 'price': '3000'},
    {'name': 'Звенигород', 'price': '1000'},
    {'name': 'Зеленоград', 'price': '500'},
    {'name': 'Ивантеевка', 'price': '1000'},
    {'name': 'Истринский район', 'price': '800'},
    {'name': 'Каширский район', 'price': '2400'},
    {'name': 'Климовск', 'price': '1400'},
    {'name': 'Клинский район', 'price': '600'},
    {'name': 'Коломенский район', 'price': '2300'},
    {'name': 'Королев', 'price': '700'},

    {'name': 'Котельники', 'price': '700'},
    {'name': 'Красноармейск', 'price': '1500'},
    {'name': 'Красногорский район', 'price': '1000'},
    {'name': 'Краснознаменск', 'price': '1700'},
    {'name': 'Ленинский район', 'price': '1400'},
    {'name': 'Лобня', 'price': '800'},
    {'name': 'Лосино-Петровский', 'price': '1300'},
    {'name': 'Лотошинский район', 'price': '1200'},
    {'name': 'Луховицкий район', 'price': '2600'},
    {'name': 'Лыткарино', 'price': '700'},
    {'name': 'Люберецкий район', 'price': '1300'},
    {'name': 'Можайский район', 'price': '1600'},
    {'name': 'Москва', 'price': '500'},
    {'name': 'Мытищинский район', 'price': '1000'},
    {'name': 'Наро-Фоминский район', 'price': '1500'},
    {'name': 'Ногинский район', 'price': '1600'},
    {'name': 'Одинцовский район', 'price': '1100'},
    {'name': 'Озерский район', 'price': '2600'},
    {'name': 'Орехово-Зуевский район', 'price': '2100'},
    {'name': 'Павлово-Посадский район', 'price': '1800'},
    {'name': 'Подольский район', 'price': '1500'},
    {'name': 'Протвино', 'price': '2100'},

    {'name': 'Пушкинский район', 'price': '1100'},
    {'name': 'Пущино', 'price': '2100'},
    {'name': 'Раменский район', 'price': '1800'},
    {'name': 'Реутов', 'price': '700'},
    {'name': 'Рошаль', 'price': '2600'},
    {'name': 'Рузский район', 'price': '1100'},
    {'name': 'Сергиево-Посадский район', 'price': '1300'},
    {'name': 'Серебряно-Прудский район', 'price': '2900'},
    {'name': 'Серпуховский район', 'price': '2100'},
    {'name': 'Солнечногорский район', 'price': '700'},
    {'name': 'Ступинский район', 'price': '2100'},
    {'name': 'Талдомский район', 'price': '1400'},
    {'name': 'Фрязино', 'price': '1200'},
    {'name': 'Химки', 'price': '500'},
    {'name': 'Черноголовка', 'price': '1600'},
    {'name': 'Чеховский район', 'price': '1800'},
    {'name': 'Шатурский район', 'price': '2800'},
    {'name': 'Шаховской район', 'price': '1400'},
    {'name': 'Щелковский район', 'price': '1400'},
    {'name': 'Электрогорск', 'price': '1700'},
    {'name': 'Электросталь', 'price': '1500'},
    {'name': 'Юбилейный', 'price': '800'},
]

list_of_paintings =[
    {'title': 'Эмаль НЦ', 'price': 550, 'image_path': 'main/img/color_baners/color_baner1.webp', 'description': 'Универсальная нитроэмаль для получения качественного защищенного покрытия. Загрунтованная поверхность изделия покрывается в два слоя, что дает до двух лет защиты от ржавчины.', 'colors': '4 цвета на выбор'},
    {'title': 'Эмаль ХВ', 'price': 650, 'image_path': 'main/img/color_baners/color_baner5.webp', 'description': 'Специализированная краска с матовым эффектом для защиты металлических изделий от возникновения ржавчины. Эмаль сочетает в себе свойства грунтовочного и финишного покрытия, что дает большую долговечность.', 'colors': '4 цвета на выбор'},
    {'title': 'Краска Hammerite', 'price': 1400, 'image_path': 'main/img/color_baners/color_baner7.webp', 'description': 'Краска польского производства. Обладает уникальным свойством нейтрализации ржавчины. Изделия сохраняют свой изначальный вид на срок до вомьми лет. Возможно нанесение с молотковым эфектом.', 'colors': '30 цветов на выбор'},
    {'title': 'Порошковое нап.', 'price': 1700, 'image_path': 'main/img/color_baners/color_baner2.webp', 'description': 'Крайне высокая степень защиты от ржавчины и повышение прочности по отношению к ударам. Дополнительная защита от вредных химических веществ и УФ-ихлучшения делает такой тип окраса практически "вечным".', 'colors': 'Любой из палитры RAL'},
    {'title': 'Грунт эмаль DALI', 'price': 1900, 'image_path': 'main/img/color_baners/color_baner3.webp', 'description': 'Специальная грунт-эмаль для черного и цветного металла. Молотковая эмаль 3 в 1. Возможно нанесение прямо по ржавчине. Высыхание за 1 час. Срок службы 10 лет.Возможно нанесение с молотковым эффектом.', 'colors': 'Любой из палитры RAL'},
    {'title': 'Эмаль WS-plast', 'price': 1900, 'image_path': 'main/img/color_baners/color_baner4.webp', 'description': 'Специальная кузнечная матовая эмаль немецкого производства высокого качества, образующая декоративный и защитный слой даже на сложных поверхностях. Срок защиты поверхности — до 10 лет.', 'colors': 'Любой из палитры RAL'},
]

ALL_CITIES = {
'решетки-на-окна-в-твери': {'title': 'Тверь', 'address': '', 'description': ''},
'решетки-на-окна-в-балашихе': {'title': 'Балашиха', 'address': '', 'description': ''},
'решетки-на-окна-в-химках': {'title': 'Химки', 'address': '', 'description': ''},
'решетки-на-окна-в-мытищах': {'title': 'Мытищи', 'address': '', 'description': ''},
'решетки-на-окна-в-люберцах': {'title': 'Люберцы', 'address': '', 'description': ''},
'решетки-на-окна-в-подольске': {'title': 'Подольск', 'address': '', 'description': ''},
'решетки-на-окна-в-красногорске': {'title': 'Красногорск', 'address': '', 'description': ''},
'решетки-на-окна-в-одинцово': {'title': 'Одинцово', 'address': '', 'description': ''},
'решетки-на-окна-в-королеве': {'title': 'Королёв', 'address': '', 'description': ''},
'решетки-на-окна-в-пушкино': {'title': 'Пушкино', 'address': '', 'description': ''},
'решетки-на-окна-в-орехово-зуево': {'title': 'Орехово-Зуево', 'address': '', 'description': ''},
'решетки-на-окна-в-клину': {'title': 'Клин', 'address': '', 'description': ''},
'решетки-на-окна-в-долгопрудном': {'title': 'Долгопрудный', 'address': '', 'description': ''},
'решетки-на-окна-в-щелково': {'title': 'Щёлково', 'address': '', 'description': ''},
'решетки-на-окна-в-домодедово': {'title': 'Домодедово', 'address': '', 'description': ''},
'решетки-на-окна-в-серпухове': {'title': 'Серпухов', 'address': '', 'description': ''},
'решетки-на-окна-в-зеленограде': {'title': 'Зеленоград', 'address': '', 'description': ''},
'решетки-на-окна-в-коломне': {'title': 'Коломна', 'address': '', 'description': ''},
'решетки-на-окна-в-раменском': {'title': 'Раменское', 'address': '', 'description': ''},
'решетки-на-окна-в-сергиев-посаде': {'title': 'Сергиев-Посад', 'address': '', 'description': ''},
'решетки-на-окна-в-реутове': {'title': 'Реутов', 'address': '', 'description': ''},
'решетки-на-окна-в-электростали': {'title': 'Электросталь', 'address': '', 'description': ''},
'решетки-на-окна-в-жуковском': {'title': 'Жуковский', 'address': '', 'description': ''},
'решетки-на-окна-в-лобне': {'title': 'Лобня', 'address': '', 'description': ''},
'решетки-на-окна-в-ивантеевке': {'title': 'Ивантеевка', 'address': '', 'description': ''},
'решетки-на-окна-в-видном': {'title': 'Видное', 'address': '', 'description': ''},
'решетки-на-окна-в-воскресенске': {'title': 'Воскресенск', 'address': '', 'description': ''},
'решетки-на-окна-в-ногинске': {'title': 'Ногинск', 'address': '', 'description': ''},
'решетки-на-окна-в-ступино': {'title': 'Ступино', 'address': '', 'description': ''},
'решетки-на-окна-в-дзержинском': {'title': 'Дзержинский', 'address': '', 'description': ''},
'решетки-на-окна-в-солнечногорске': {'title': 'Солнечногорск', 'address': '', 'description': ''},
'решетки-на-окна-в-дмитрове': {'title': 'Дмитров', 'address': '', 'description': ''},
'решетки-на-окна-в-лыткарино': {'title': 'Лыткарино', 'address': '', 'description': ''},
'решетки-на-окна-в-дедовске': {'title': 'Дедовск', 'address': '', 'description': ''},
'решетки-на-окна-в-хотьково': {'title': 'Хотьково', 'address': '', 'description': ''},
'решетки-на-окна-в-железнодорожном': {'title': 'Железнодорожный', 'address': '', 'description': ''},
'решетки-на-окна-в-дубне': {'title': 'Дубна', 'address': '', 'description': ''},
'решетки-на-окна-в-чехове': {'title': 'Чехов', 'address': '', 'description': ''},
'решетки-на-окна-в-фрязино': {'title': 'Фрязино', 'address': '', 'description': ''},
'решетки-на-окна-в-лосино-петровском': {'title': 'Лосино-Петровский', 'address': '', 'description': ''},
'решетки-на-окна-в-павловском-посаде': {'title': 'Павловский посад', 'address': '', 'description': ''} ,
'решетки-на-окна-в-краснознаменске': {'title': 'Краснознаменск', 'address': '', 'description': ''},
'решетки-на-окна-в-звенигороде': {'title': 'Звенигород', 'address': '', 'description': ''},
'решетки-на-окна-в-старой-купавне': {'title': 'Старая Купавна', 'address': '', 'description': ''} ,
'решетки-на-окна-в-электрогорске': {'title': 'Электрогорск', 'address': '', 'description': ''},
'решетки-на-окна-в-апрелевке': {'title': 'Апрелевка', 'address': '', 'description': ''},
'решетки-на-окна-в-троицке': {'title': 'Троицк', 'address': '', 'description': ''},
'решетки-на-окна-в-щербинке': {'title': 'Щербинка', 'address': '', 'description': ''},
'решетки-на-окна-в-пущино': {'title': 'Пущино', 'address': '', 'description': ''},
'решетки-на-окна-в-можайске': {'title': 'Можайск', 'address': '', 'description': ''},
'решетки-на-окна-в-черноголовке': {'title': 'Черноголовка', 'address': '', 'description': ''},
'решетки-на-окна-в-голицыно': {'title': 'Голицыно', 'address': '', 'description': ''},
'решетки-на-окна-в-кашире': {'title': 'Кашира', 'address': '', 'description': ''},
'решетки-на-окна-в-истре': {'title': 'Истра', 'address': '', 'description': ''},
'решетки-на-окна-в-электроуглях': {'title': 'Электроугли', 'address': '', 'description': ''},
'решетки-на-окна-в-егорьевске': {'title': 'Егорьевск', 'address': '', 'description': ''},
'решетки-на-окна-в-протвино': {'title': 'Протвино', 'address': '', 'description': ''},
'решетки-на-окна-в-наро-фоминске': {'title': 'Наро-Фоминск', 'address': '', 'description': ''},
'решетки-на-окна-в-луховицах': {'title': 'Луховицы', 'address': '', 'description': ''},
'решетки-на-окна-в-шатуре': {'title': 'Шатура', 'address': '', 'description': ''},
'решетки-на-окна-в-волоколамске': {'title': 'Волоколамск', 'address': '', 'description': ''},
'решетки-на-окна-в-кубинке': {'title': 'Кубинка', 'address': '', 'description': ''},
'решетки-на-окна-в-бронницах': {'title': 'Бронницы', 'address': '', 'description': ''},
'решетки-на-окна-в-зарайске': {'title': 'Зарайск', 'address': '', 'description': ''},
'решетки-на-окна-в-рузе': {'title': 'Руза', 'address': '', 'description': ''},
'решетки-на-окна-в-красноармейске': {'title': 'Красноармейск', 'address': '', 'description': ''},
'решетки-на-окна-в-пересвете': {'title': 'Пересвет', 'address': '', 'description': ''},
'решетки-на-окна-в-котельниках': {'title': 'Котельники', 'address': '', 'description': ''},
'решетки-на-окна-в-московском': {'title': 'Московский', 'address': '', 'description': ''},
'решетки-на-окна-в-климовске': {'title': 'Климовск', 'address': '', 'description': ''},
'решетки-на-окна-в-ликино-дулево': {'title': 'Ликино-Дулёво', 'address': '', 'description': ''},
'решетки-на-окна-в-озерах': {'title': 'Озёры', 'address': '', 'description': ''},
'решетки-на-окна-в-купавне': {'title': 'Купавна', 'address': '', 'description': ''},
'решетки-на-окна-в-рошали': {'title': 'Рошаль', 'address': '', 'description': ''},
'решетки-на-окна-в-куровском': {'title': 'Куровское', 'address': '', 'description': ''},
'решетки-на-окна-в-талдоме': {'title': 'Талдом', 'address': '', 'description': ''},
'решетки-на-окна-в-краснозаводске': {'title': 'Краснозаводск', 'address': '', 'description': ''},
'решетки-на-окна-в-яхроме': {'title': 'Яхрома', 'address': '', 'description': ''},
'решетки-на-окна-в-высоковске': {'title': 'Высоковск', 'address': '', 'description': ''},
'решетки-на-окна-в-дрезне': {'title': 'Дрезна', 'address': '', 'description': ''},
'решетки-на-окна-в-верее': {'title': 'Верея', 'address': '', 'description': ''},
}

ALL_CATEGORIES = [1, 2, 3, 4, 5, 6, 7, 8]
russian_categories = {
    # all grids
    "металлические-решетки-на-окна": {"title": "Все металлические решетки на окна", "number_of_category": ALL_CATEGORIES, 'text': 'металлические-решетки-на-окна.html'},

    #list_of_grids_purpose
    "решетки-на-балкон": {"title": "Металлические решетки на балкон", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-на-балкон.html'},
    "решетки-на-приямки": {"title": "Металлические решетки на приямки", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-на-приямки.html'},
    "решетки-на-лоджию": {"title": "Металлические решетки на лоджию", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-на-лоджию.html'},
    "решетки-для-квартиры": {"title": "Металлические решетки на окна квартиры", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-для-квартиры.html'},
    "решетки-на-первый-этаж": {"title": "Металлические решетки на окна первого этажа", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-на-первый-этаж.html'},
    "решетки-для-цоколя": {"title": "Металлические решетки на цоколь или в подвал", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-для-цоколя.html'},
    "решетки-для-дома": {"title": "Металлические решетки на окна дома", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-для-дома.html'},
    "решетки-от-выпадения-детей": {"title": "Металлические решетки на окна от выпадения детей (кид-стоп)", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-от-выпадения-детей.html'},
    "решетки-на-кондиционер": {"title": "Металлические решетки на кондиционер", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-на-кондиционер.html'},
    "внутренние-решетки": {"title": "Внутренние металлические решетки на окна", "number_of_category": ALL_CATEGORIES, 'text': 'внутренние-решетки.html'},
    "решетки-для-дачи": {"title": "Металлические решетки на окна для дачи", "number_of_category": ALL_CATEGORIES, 'text': 'решетки-для-дачи.html'},

    #list_of_categories
    "решетки-на-окна-эконом-класс": {"title": "Металлические решетки на окна эконом класс", "number_of_category": [1], 'text': 'решетки-на-окна-эконом-класс.html'},
    "дутые-решетки-на-окна-эконом-класс": {"title": "Дутые эконом металлические решетки на окна", "number_of_category": [2], 'text': 'решетки-на-окна-эконом-класс.html'},
    "дутые-и-обычные-решетки-на-окна-эконом-класс": {"title": "Дутые и обычные эконом металлические решетки на окна", "number_of_category": [1, 2], 'text': 'решетки-на-окна-эконом-класс.html'},
    "ажурные-решетки-на-окна": {"title": "Ажурные металлические решетки на окна", "number_of_category": [3], 'text': 'ажурные-решетки-на-окна.html'},
    "дутые-ажурные-решетки": {"title": "Дутые ажурные металлические решетки на окна", "number_of_category": [4], 'text': 'ажурные-решетки-на-окна.html'},
    "дутые-и-обычные-ажурные-решетки": {"title": "Дутые и обычные ажурные металлические решетки на окна", "number_of_category": [3, 4], 'text': 'ажурные-решетки-на-окна.html'},
    "решетки-на-окна-вип-класс": {"title": "Металлические решетки на окна vip класс", "number_of_category": [5], 'text': 'решетки-на-окна-вип-класс.html'},
    "дутые-решетки-вип-класса": {"title": "Дутые металлические решетки на окна vip класс", "number_of_category": [6], 'text': 'решетки-на-окна-вип-класс.html'},
    "дутые-и-обычные-решетки-вип-класса": {"title": "Дутые и обычные металлические решетки на окна vip класс", "number_of_category": [5, 6], 'text': 'решетки-на-окна-вип-класс.html'},
    "эксклюзивные-кованые-решетки": {"title": "Металлические решетки на окна эксклюзив", "number_of_category": [7], 'text': 'эксклюзивные-кованые-решетки.html'},
    "дутые-эксклюзивные-решетки": {"title": "Дутые металлические решетки на окна эксклюзив", "number_of_category": [8], 'text': 'эксклюзивные-кованые-решетки.html'},
    "дутые-и-обычные-эксклюзивные-решетки": {"title": "Дутые и обычные металлические решетки на окна эксклюзив", "number_of_category": [7, 8], 'text': 'эксклюзивные-кованые-решетки.html'},

    #list_of_classes
    "дутые-решетки-на-окна": {"title": "Дутые металлические решетки на окна", "number_of_category": [2, 4, 6, 8], 'text': 'дутые-решетки-на-окна.html'},
    "решетки-на-окна-без-дутости": {"title": "Прямые металлические решетки на окна","number_of_category": [1, 3, 5, 7], 'text': 'решетки-на-окна-без-дутости.html'},


    #list_of_open_types
    "арочные-решетки-на-окна": {"title": "Арочные металлические решетки на окна", "number_of_category": ALL_CATEGORIES, 'text': 'арочные-решетки-на-окна.html'},
    "распашные-решетки-на-окна": {"title": "Распашные металлические решетки на окна", "number_of_category": ALL_CATEGORIES, 'text': 'металлические-решетки-на-окна.html'},
    "решетки-без-открывания": {"title": "Металлические решетки на окна без открывания", "number_of_category": ALL_CATEGORIES, 'text': 'металлические-решетки-на-окна.html'},

    #list_of_kinds
    "сварные-решетки-на-окна": {"title": "Сварные металлические решетки на окна", "number_of_category": [1, 3], 'text': 'сварные-решетки-на-окна.html'},
    "кованые-решетки-на-окна": {"title": "Кованые металлические решетки на окна", "number_of_category": [5, 7], 'text': 'кованые-решетки-на-окна.html'},

    #list_of_popular_sections
    "топ-100-кованых-оконных-решеток": {"title": "Кованые оконные решетки | топ - 100 эскизов", "number_of_category": [5,6,7,8], 'text': 'металлические-решетки-на-окна.html'},
    "топ-100-сварных-решеток-на-окна": {"title": "Сварные оконные решетки | топ - 100 эскизов", "number_of_category": [1,2,3,4], 'text': 'металлические-решетки-на-окна.html'},
}

product_category_texts = {
    1: 'main/text/product_category_texts/сварные.html',
    2: 'main/text/product_category_texts/сварные-дутые.html',
    3: 'main/text/product_category_texts/ажурные.html',
    4: 'main/text/product_category_texts/ажурные-дутые.html',
    5: 'main/text/product_category_texts/кованые.html',
    6: 'main/text/product_category_texts/кованые-дутые.html',
    7: 'main/text/product_category_texts/эксклюзив.html',
    8: 'main/text/product_category_texts/эксклюзив-дутые.html',
}

# one day cache will be stored
TTL_OF_CACHE_SECONDS = 60 * 60 * 24

def get_paginated_url(request, page_number):
    params = request.GET.copy()
    params['page'] = page_number
    return f"{request.path}?{urlencode(params)}"

def get_products_by_categories(category_number, min_price, max_price, order_by_name, order_scending, limit):
    cache_key = "category_" + str(category_number) + "_" + str(min_price) + \
                str(max_price) + order_by_name + order_scending + str(limit)
    products_list_from_cache = cache.get(cache_key)
    if products_list_from_cache:
        return products_list_from_cache

    order_by_name = order_by_name if order_scending == 'asc' else '-' + order_by_name
    # в прошлых версиях проекта GIT можно найти SQL запрос аналогичный этому ОРМ запросу
    queryset = PriceWinguardMain.objects.filter(
        price_winguard_sketch__category__in=category_number
    ).annotate(
        percent=(F('price_winguard_sketch__id') % 3 + 1) * 10 + (F('price_winguard_sketch__id') % 2 * 5),
        stars_count=(F('price_winguard_sketch__id') % 10 + F('price_winguard_sketch__id') % 3 + F('price_winguard_sketch__id') % 7 + F('price_winguard_sketch__id') % 5 + F('price_winguard_sketch__id') % 11),
        path_folder=F('price_winguard_sketch__category'),
        path_file=F('price_winguard_sketch__number'),
        price=F('price_b2c'),
        saleprice=Round(F('price_b2c') / (1 - F('percent') / 100), -1),
        popularity=F('price_winguard_sketch__popularity')
    ).values('price_winguard_sketch__id').annotate(
        id=F('price_winguard_sketch__id'),
        percent=Min('percent'),
        stars_count=Min('stars_count'),
        path_folder=Min('path_folder'),
        path_file=Min('path_file'),
        price=Min('price_b2c'),
        saleprice=Min('saleprice'),
        popularity=Min('popularity')
    ).filter(
        price__gt=min_price,
        price__lt=max_price
    ).order_by(f'{order_by_name}')[:limit]
    cache.set(cache_key, queryset, TTL_OF_CACHE_SECONDS)
    return queryset


def get_product_by_sketch_category_and_number(category, number):
    if isinstance(category, int):
        category = [category]
    cache_key = "product_" + str(category) + "_" + str(number)
    product = cache.get(cache_key)
    if product:
        return product
    product = PriceWinguardMain.objects.filter(
        price_winguard_sketch__category__in=category,
        price_winguard_sketch__number=number
    ).annotate(
        percent=(F('price_winguard_sketch__id') % 3 + 1) * 10 + (F('price_winguard_sketch__id') % 2 * 5),
        stars_count=(F('price_winguard_sketch__id') % 10 + F('price_winguard_sketch__id') % 3 + F(
            'price_winguard_sketch__id') % 7 + F('price_winguard_sketch__id') % 5 + F(
            'price_winguard_sketch__id') % 11),
        path_folder=F('price_winguard_sketch__category'),
        path_file=F('price_winguard_sketch__number'),
        price=F('price_b2c'),
        saleprice=Round(F('price_b2c') / (1 - F('percent') / 100), -1)
    )
    cache.set(cache_key, product, TTL_OF_CACHE_SECONDS)
    return product




def get_folder_of_photos_by_category_and_number(category, numberOfProduct):
    return os.path.join(base_dir, f'main/static/main/img/projects/{category}/{category}-{numberOfProduct}')


def get_product_project_photos_eight(category, numberOfProduct):
    initialNumberOfProduct = numberOfProduct
    numberOfProduct = 0
    try:
        img_list = os.listdir(get_folder_of_photos_by_category_and_number(category, initialNumberOfProduct))
    except:
        img_list = []
    for i in range(len(img_list)):
        img_list[i] = f'projects/{category}/{category}-{initialNumberOfProduct}/' + img_list[i]
    while len(img_list) < 8 and numberOfProduct < 200: # TODO: отвратительный хардкод пофиксить когда будут фотки работ
        numberOfProduct = numberOfProduct + 1
        if numberOfProduct == initialNumberOfProduct:
            continue
        path_of_file = f'projects/{category}/{category}-{numberOfProduct}/1.webp'
        if os.path.isfile(os.path.join(img_dir,path_of_file)):
            img_list.append(path_of_file)
    return img_list


def count_products_by_category(category_number):
    cache_key = "count_" + str(category_number)
    count = cache.get(cache_key)
    if count is None:
        count = PriceWinguardSketch.objects.filter(category=category_number).count()
        cache.set(cache_key, count, TTL_OF_CACHE_SECONDS)
    return count


def get_categories_min_price(category_number):
    cache_key = "min_price_" + str(category_number)
    min_price = cache.get(cache_key)
    if min_price is None:
        min_price = \
            PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_number).aggregate(
                Min('price_b2c'))[
                'price_b2c__min']
        cache.set(cache_key, min_price, TTL_OF_CACHE_SECONDS)
    return min_price


def get_categories_max_price(category_number):
    cache_key = "max_price_" + str(category_number)
    max_price = cache.get(cache_key)
    if max_price is None:
        max_price = PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_number).values(
            'price_winguard_sketch__id') \
            .annotate(min_price=Min('price_b2c')).values('min_price').aggregate(Max('min_price'))['min_price__max']
        cache.set(cache_key, max_price, TTL_OF_CACHE_SECONDS)
    return max_price


count = {
    "economy": count_products_by_category(1) + count_products_by_category(2),
    "ajur": count_products_by_category(3) + count_products_by_category(4),
    "vip": count_products_by_category(5) + count_products_by_category(6),
    "exlusive": count_products_by_category(7) + count_products_by_category(8),
    'amount_of_all': count_products_by_category(1) + count_products_by_category(2) + count_products_by_category(3) +
                     count_products_by_category(4) + count_products_by_category(5) + count_products_by_category(6) +
                     count_products_by_category(7) + count_products_by_category(8)
}

def get_POST_parameter(name_of_parameter, request):
    name_getter = request.POST.get(name_of_parameter)
    return name_getter if name_getter else ''

def handle_post_request(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        name = get_POST_parameter('name', request)
        additional_info = get_POST_parameter('additional_info', request)
        if 'заказ решетки' in subject:
            number = get_POST_parameter('number_str', request)
            open_type = 'Открывающаяся' if 'on' in get_POST_parameter('open_type', request) else get_POST_parameter('open_type', request)
            width = get_POST_parameter('width', request)
            height = get_POST_parameter('height', request)
            width_of_rod = get_POST_parameter('width_of_rod', request)
            painting = 'Нитро-эмаль' if 'on' in get_POST_parameter('painting', request) else get_POST_parameter('painting', request)
            amount = get_POST_parameter('amount', request)
            installing = get_POST_parameter('installing', request)
            price = get_POST_parameter('price', request)
            additional_info = f'Решетка на заказ: {number} \n' \
                              f'Длина решетки в см: {width}\n' \
                              f'Высота решетки в см: {height}\n' \
                              f'Ширина прутка: {width_of_rod}\n' \
                              f'Тип открывания: {open_type}\n' \
                              f'Покраска: {painting}\n' \
                              f'Количество: {amount}\n' \
                              f'Ожидаемая клиентом цена: {price}\n'
        if phone != '' and phone != None and subject != '' and subject != None:
            # Send data via HTTP POST request
            url = 'https://svarnik.ru/bx24/'
            headers = {'User-Agent': 'Reforgebot/1.0'}
            data = {
                'ikey': 'WqfnDx7soB1iVn3K1ybM',
                'domain': 'оконные-решётки.рф',
                'roistat': 'nocookie',
                'subject': subject,
                'name': name,
                'phone': phone,
                'additional_info': additional_info,
            }
            try:
                response = requests.post(url, headers=headers, data=data)
                print(response)
            except Exception as e:
                print(e)
                pass
            return redirect('index')


def index(request):
    if request.method == 'POST':
        handle_post_request(request)
    leaders_of_selling = get_products_by_categories(ALL_CATEGORIES, 0, 99999, 'popularity', 'desc', 16)
    min_price_1 = get_categories_min_price([1])
    min_price_2 = get_categories_min_price([3])
    min_price_3 = get_categories_min_price([5])
    min_price_4 = get_categories_min_price([7])
    short_list_of_reviews = list_of_reviews[:4]
    short_list_of_reviews_collapsed = list_of_reviews_collapsed[:8]
    meta_description = 'Решетки на окна для квартиры и дачи по ценам от производителя. ' \
                       'Бесплатная консультация и изготовление по вашим размерам. Гарантия 5 лет.'
    context = {
        'title': 'Металлические решетки на окна с установкой',
        'meta_description': meta_description,
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

    products_list = []
    if "топ" in category:
        products_list = get_products_by_categories(category["number_of_category"], min_price_for_sort,
                                                   max_price_for_sort,
                                                   order_type, order_scending, limit)
    else:
        products_list = get_products_by_categories(category["number_of_category"], min_price_for_sort,
                                                   max_price_for_sort,
                                                   order_type, order_scending, limit)
    min_price = get_categories_min_price(category["number_of_category"])
    max_price = get_categories_max_price(category["number_of_category"])

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 45)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    leaders_of_selling = get_products_by_categories(ALL_CATEGORIES, 0, 99999, 'popularity', 'desc', 16)
    text_for_category = 'main/text/' + category['text']
    meta_description = 'Решетки на окна по разным ценам. Популярные эскизы со скидками. ' \
                       'Сварные, ажурные, кованые и дутые решетки по размерам клиента.'
    context = {
        'title': category['title'] + ' страница ' + str(page),
        'meta_description': meta_description,
        'text_for_category': text_for_category,
        'list_of_reviews': list_of_reviews,
        'products': products, 'category': category,
        'leaders_of_selling': leaders_of_selling,
        'min_price': min_price, 'max_price': max_price, 'list_of_photos_done': list_of_photos_done,


        # for pagination
        'prev_url': get_paginated_url(request, products.previous_page_number()) if products.has_previous() else None,
        'next_url': get_paginated_url(request, products.next_page_number()) if products.has_next() else None,

        'count': count,
    }
    return render(request, 'main/catalog-category.html', context)


def contacts(request):
    meta_description = 'Металлические решетки по хорошей цене. Собственное производство в Клинском районе. ' \
                       'Бесплатная консультация по телефону: +7-495-374-53-64'
    context = {
        'title': 'Контакты',
        'meta_description': meta_description,
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
    similar_grids_by_price = get_products_by_categories([first_row_product.path_folder],
                                                        first_row_product.price_b2c - price_step_for_category[
                                                            first_row_product.path_folder],
                                                        first_row_product.price_b2c + price_step_for_category[
                                                            first_row_product.path_folder],
                                                        'price', 'asc', 15)
    photos_of_projects = get_product_project_photos_eight(first_row_product.path_folder, first_row_product.path_file)
    text_for_product = product_category_texts[category]
    requests.get('http://92.63.107.238/get.php', params={'tbl': 'price_winguard_sketch', 'id':first_row_product.price_winguard_sketch_id}) #increase popularity of item by 1
    meta_description = 'Металлическая решетка ' + str(first_row_product.path_folder) + '-' + str(first_row_product.path_file) \
                       + ' со скидкой. Фотографии работ и отзывы клиентов.' \
                       ' Покраска, покрытие, напыление по дешевой цене. Гарантия до 50 лет.'
    context = {
        'title': 'Решетка на окно ' + str(first_row_product.path_folder) + '-' + str(first_row_product.path_file),
        'meta_description': meta_description,
        'text_for_product': text_for_product,
        'product': product,
        'list_of_open_types_for_calculator': list_of_open_types_for_calculator,
        'list_of_reviews': list_of_reviews,
        'similar_grids_by_price': similar_grids_by_price,
        'photos_of_projects': photos_of_projects,
        'count': count
    }
    return render(request, 'main/product.html', context)


def projects(request):
    meta_description = 'Более 1000 довольных клиентов. Фотографии работ и возможность заказать такую же решетку. ' \
                       'Бесплатная консультация и замер.'
    context = {
        'title': 'Наши работы',
        'meta_description': meta_description,
        'list_of_photos_done': list_of_photos_done,
        'list_of_photos_done_collapsed': list_of_photos_done_collapsed,
        'count': count
    }
    return render(request, 'main/projects.html', context)


def reviews(request):
    meta_description = 'Отзывы клиентов о металлических решетках. Персональные скидки за оставленный комментарий. ' \
                       'Большой опыт в ковке и сварке решеток на окна.'
    context = {
        'title': 'Отзывы клиентов',
        'meta_description': meta_description,
        'list_of_reviews': list_of_reviews,
        'list_of_reviews_collapsed': list_of_reviews_collapsed,
        'count': count
    }
    return render(request, 'main/reviews.html', context)


def compare(request):
    str_of_cookies = request.COOKIES.get('Compare')
    list_of_compares = []
    if str_of_cookies != '' and str_of_cookies != None:
        list_of_compares_cookie = str_of_cookies.split(',')
        for sketch_id in list_of_compares_cookie:
            product = {"id": sketch_id}
            product["price"] = \
                PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c')[0]['price_b2c']
            product["percent"] = (int(product["id"]) % 3 + 1) * 10 + (int(product["id"]) % 2) * 5
            product["saleprice"] = int(product["price"] * (1 + product["percent"] / 100))
            path = "".join(
                re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
            path_arr = path.split("/")
            product["path_folder"] = path_arr[1]
            product["path_file"] = path_arr[2]
            product['additional_info'] = list(
                PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c', 'name'))
            list_of_compares.append(product)
    meta_description = 'Сравнить решетки по цене, материалу, покраске, типу открывания. ' \
                       'Компания предоставляет большой выбор металлических решеток на окна.'
    context = {
        'title': 'Сравнение решеток',
        'meta_description': meta_description,
        'products': list_of_compares,
        'count': count
    }
    return render(request, 'main/compare.html', context)


def favorite(request):
    str_of_cookies = request.COOKIES.get('Favorites')
    list_of_favorites = []
    if str_of_cookies != '' and str_of_cookies != None:
        list_of_favorites_cookie = str_of_cookies.split(',')
        for sketch_id in list_of_favorites_cookie:
            product = {"id": sketch_id}
            product["price"] = \
                PriceWinguardMain.objects.filter(price_winguard_sketch_id=product["id"]).values('price_b2c')[0]['price_b2c']
            product["percent"] = (int(product["id"]) % 3 + 1) * 10 + (int(product["id"]) % 2) * 5
            product["saleprice"] = int(product["price"] * (1 + product["percent"] / 100))
            path = "".join(
                re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=product["id"]).path))
            path_arr = path.split("/")
            product["path_folder"] = path_arr[1]
            product["path_file"] = path_arr[2]
            list_of_favorites.append(product)
    meta_description = 'Понравившиеся металлические решетки. Выбирайте любой эскиз и добавляйте его в свой список. ' \
                       'Возможен заказ сразу нескольких видов изделий.'
    context = {
        'title': 'Избранные решетки',
        'meta_description': meta_description,
        'products': list_of_favorites,
        'count': count
    }
    return render(request, 'main/favorite.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("Page NOT found")


def privacy(request):
    meta_description = 'Политика конфиденциальности компании на сайте оконные-решетки.рф . Совершая покупку, вы соглашаетесь на обработку персональных данных.'
    context = {
        'title': 'Конфиденциальность',
        'meta_description': meta_description,
        'count': count
    }
    return render(request, 'main/privacy.html', context)

def sales(request):
    meta_description = 'Скидка 20% при полной предоплате металлической решетки. ' \
                       'Скидка 10% при оплате в день приезда замерщика. Бесплатная консультация и замер.'
    context = {
        'title': 'Акции',
        'meta_description': meta_description,
        'list_of_sales_items': list_of_sales_items
    }
    return render(request, 'main/sales.html', context)

def delivery(request):
    meta_description = 'Доставка по всей Московской области. Для расчета цены на металлические решетки на окна звоните по телефону +7(495) 374 53 64'
    context = {
        'title': 'Доставка',
        'list_of_deliveries': list_of_deliveries,
        'meta_description': meta_description
    }
    return render(request, 'main/delivery.html', context)

def installing(request):
    meta_description = 'Установка металлических решеток на окна по всей Московкой области. Демонтаж старой решетки и монтаж новой за 3000 руб.'
    context = {
        'title': 'Установка',
        'meta_description': meta_description
    }
    return render(request, 'main/installing.html', context)

def paying(request):
    meta_description = 'Оплата заказа наличными, картой, онлайн банком, счетом юридического лица. Оплата решетки производится после установки.'
    context = {
        'title': 'Оплата',
        'meta_description': meta_description
    }
    return render(request, 'main/paying.html', context)

def guarantee(request):
    meta_description = 'Гарантия на решетки на окна. Гарантия на продукцию производителя сроком до нескольких лет.'
    context = {
        'title': 'Гарантия',
        'meta_description': meta_description
    }
    return render(request, 'main/guarantee.html', context)

def order_scheme(request):
    meta_description = 'Схема заказа оконный решеток на окна'
    context = {
        'title': 'Схема заказа',
        'meta_description': meta_description
    }
    return render(request, 'main/order_scheme.html', context)

def faq(request):
    meta_description = 'Частые вопросы по изготовлению и установке решеток на окна.'
    context = {
        'title': 'Вопрос-ответ',
        'meta_description': meta_description
    }
    return render(request, 'main/faq.html', context)

def about(request):
    meta_description = 'Информация о компании оконные-решётки.рф'
    short_list_of_reviews = list_of_reviews[:4]
    short_list_of_reviews_collapsed = list_of_reviews_collapsed[:8]
    context = {
        'title': 'О компании',
        'short_list_of_reviews': short_list_of_reviews,
        'short_list_of_reviews_collapsed': short_list_of_reviews_collapsed,
        'meta_description': meta_description
    }
    return render(request, 'main/about.html', context)


def color(request):
    meta_description = 'Покраска решеток на окна.'
    context = {
        'title': 'Покраска',
        'meta_description': meta_description,
        'list_of_sales_items': list_of_sales_items,
        'list_of_paintings': list_of_paintings,
    }
    return render(request, 'main/color.html', context)