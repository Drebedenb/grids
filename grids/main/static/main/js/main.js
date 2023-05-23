//перезагружать страницу каждый раз, когда пользователь нажимает кнопку назад в истории браузера
window.addEventListener( "pageshow", function ( event ) {
  const historyTraversal = event.persisted ||
                         ( typeof window.performance != "undefined" &&
                              window.performance.getEntriesByType("navigation")[0].type === "back_forward" );
  if ( historyTraversal ) {
    window.location.reload();
  }
});


let introSwiper = new Swiper("#intro-swiper", {
    loop: true,
    effect: "fade",
    fadeEffect: {
        crossFade: true
    },
    navigation: {
        prevEl: "#intro-swiper-control .btn-swiper-prev",
        nextEl: "#intro-swiper-control .btn-swiper-next"
    }
});

let reasonsSwiper = new Swiper("#reasons-swiper", {
    slidesPerView: 1,
    slidesPerGroup: 1,
    spaceBetween: 20,
    navigation: {
        prevEl: "#reasons-swiper-control .btn-swiper-prev",
        nextEl: "#reasons-swiper-control .btn-swiper-next"
    },
    breakpoints: {
        576: {
            slidesPerView: 1,
            slidesPerGroup: 1,
            spaceBetween: 20
        },
        992: {
            slidesPerView: 2,
            slidesPerGroup: 2,
            spaceBetween: 20
        },
        1200: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 30
        },
        1400: {
            slidesPerView: 5,
            slidesPerGroup: 5,
            spaceBetween: 25
        }
    }
});

let featuresSwiper = new Swiper("#features-swiper", {
    slidesPerView: 2,
    slidesPerGroup: 2,
    spaceBetween: 20,
    navigation: {
        // prevEl: "#features-swiper-control #features-swiper-control_mobile .btn-swiper-prev",
        // nextEl: "#features-swiper-control #features-swiper-control_mobile .btn-swiper-next"

        prevEl: "#features-swiper-control .btn-swiper-prev",
        nextEl: "#features-swiper-control .btn-swiper-next"
    },
    breakpoints: {
        576: {
            slidesPerView: 2,
            slidesPerGroup: 2,
            spaceBetween: 25
        },
        992: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 25
        },
        1200: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 25
        },
        1400: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 25
        }
    }
});


let teamSwiper = new Swiper("#team-swiper", {
    loop: true,
    effect: "fade",
    fadeEffect: {
        crossFade: true
    },
    navigation: {
        prevEl: "#team-swiper-control .btn-swiper-prev",
        nextEl: "#team-swiper-control .btn-swiper-next"
    }
});


let banerSwiper = new Swiper("#baner-swiper", {
    loop: true,
    effect: "fade",
    fadeEffect: {
        crossFade: true
    },
    navigation: {
        prevEl: "#team-swiper-baner_control",
        nextEl: "#team-swiper-baner_control"
    }
});


let projectsSwiper = new Swiper("#projects-swiper", {
    loop: true,
    effect: "fade",
    fadeEffect: {
        crossFade: true
    },
    navigation: {
        prevEl: "#projects-swiper-control .btn-swiper-prev",
        nextEl: "#projects-swiper-control .btn-swiper-next"
    }
});

let productSwiper = new Swiper("#product-swiper", {
    navigation: {
        prevEl: "#product-swiper-control .btn-swiper-prev",
        nextEl: "#product-swiper-control .btn-swiper-next"
    },
    pagination: {
        el: "#product-swiper-control .swiper-pagination",
        type: "bullets",
        clickable: true
    }
});

let productSwiper2 = new Swiper("#product-swiper2", {
    navigation: {
        prevEl: "#product-swiper-control2 .btn-swiper-prev",
        nextEl: "#product-swiper-control2 .btn-swiper-next"
    },
    pagination: {
        el: "#product-swiper-control2 .swiper-pagination",
        type: "bullets",
        clickable: true
    }
});

//блок кода о  кукисах
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

//конец блока кода о кукисах

//блок кода о добавлении в избранное
function paintHeartRed(className) {
    let items = document.getElementsByClassName(className);
    for (let i = 0; i < items.length; i++) {
        items[i].children[0].style.fill = '#F5320E';
        items[i].children[0].style.stroke = '#F5320E';
    }
}

function paintHeartGrey(className) {
    let items = document.getElementsByClassName(className);
    for (let i = 0; i < items.length; i++) {
         items[i].children[0].style.fill = 'none';
         items[i].children[0].style.stroke = '#959595';
    }
}

function changeFavoriteList(element) {
    let heartClassName; //heart-(number) example: heart-1, heart-193
    for (let i = 0; i < element.classList.length; i++) {
        if (element.classList[i].includes('heart')) heartClassName = element.classList[i]
    }
    let idOfProduct = heartClassName.match(/\d+/)[0]
    let cookieName = "Favorites"
    let stringOfFavorite = getCookie(cookieName)
    if (!stringOfFavorite) {
        paintHeartRed(heartClassName)
        setCookie(cookieName, [idOfProduct], 7)
        callSnackbar('Вы добавили товар в избранное')
    } else if (stringOfFavorite.includes(idOfProduct)) {
        let str = stringOfFavorite.split(',').filter(item => item !== idOfProduct).join(',')
        paintHeartGrey(heartClassName)
        setCookie(cookieName, [str], 7)
        callSnackbar('Вы убрали товар из избранного')
    } else {
        paintHeartRed(heartClassName)
        setCookie(cookieName, [stringOfFavorite, idOfProduct], 7)
        callSnackbar('Вы добавили товар в избранное')
    }
    changeFavoriteCounter();
}

function getAmountOfFavorite() {
    let str = getCookie("Favorites")
    return str === "" || str === null ? 0 : str.split(",").length
}

function changeFavoriteCounter() {
    document.getElementById("amountOfFavorite").textContent = getAmountOfFavorite().toString()
}

function changeFavoriteCounterAndPaintHearts() {
    changeFavoriteCounter();//вызываем при начальной за грузке любой страницы
    let favoritesStr = getCookie("Favorites")
    let favorites;
    if ( favoritesStr === '' || favoritesStr === null) {
        favorites = []
    } else {
        favorites = favoritesStr.split(',')
    }
    // let favorites = favoritesStr === '' ? [] : 
    for (const productId of favorites) {
        try {
            paintHeartRed("heart-" + productId)
        } catch (e) {
        }
    }
}
changeFavoriteCounterAndPaintHearts()
//конец блока кода о добавлении в избранное

//блок кода о добавлении в сравнение
function paintChartRed(className) {
    let items = document.getElementsByClassName(className);
    for (let i = 0; i < items.length; i++) {
        items[i].style.fill = '#F5320E';
        items[i].style.stroke = '#F5320E';
    }
}

function paintChartGrey(className) {
    let items = document.getElementsByClassName(className);
    for (let i = 0; i < items.length; i++) {
        items[i].style.fill = 'none';
        items[i].style.stroke = '#959595';
    }
}

function changeCompareList(element) {
    let chartClassName; //chart-(number) example: chart-1, chart-193
    for (let i = 0; i < element.classList.length; i++) {
        if (element.classList[i].includes('chart')) chartClassName = element.classList[i]
    }
    let idOfProduct = chartClassName.match(/\d+/)[0]
    let cookieName = "Compare"
    let stringOfCompare = getCookie(cookieName)
    if (!stringOfCompare) {
        paintChartRed(chartClassName)
        setCookie(cookieName, [idOfProduct], 7)
        callSnackbar('Вы добавили товар в сравнение')
    } else if (stringOfCompare.includes(idOfProduct)) {
        let str = stringOfCompare.split(',').filter(item => item !== idOfProduct).join(',')
        paintChartGrey(chartClassName)
        setCookie(cookieName, [str], 7)
        callSnackbar('Вы убрали товар из сравнения')
    } else {
        paintChartRed(chartClassName)
        setCookie(cookieName, [stringOfCompare, idOfProduct], 7)
        callSnackbar('Вы добавили товар в сравнение')
    }
    changeCompareCounter();
}

function getAmountOfCompare() {
    let str = getCookie("Compare")
    return str === "" || str === null ? 0 : str.split(",").length
}

function changeCompareCounter() {
    document.getElementById("amountOfCompare").textContent = getAmountOfCompare().toString()
}

function changeCompareCounterAndPaintCompares() {
    changeCompareCounter();//вызываем при начальной загрузке любой страницы
    let comparesStr = getCookie("Compare")
    let compares;
    if ( comparesStr === '' || comparesStr === null) {
        compares = []
    } else {
        compares = comparesStr.split(',')
    }
    // let compares = comparesStr === '' ? [] : comparesStr.split(',')
    for (const productId of compares) {
        try {
            paintChartRed("chart-" + productId)
        } catch (e) {
        }
    }
}
changeCompareCounterAndPaintCompares()

//конец блока кода о добавлении в сравнение

//блок кода о снекбаре
function callSnackbar(text) {
    const x = document.getElementById("snackbar");
    x.textContent = text;
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
}

//конец блока кода о снекбаре

//НИЖЕ ДЛЯ ФАЙЛА catalog-category
//блок кода о фильтрации
let priceSlider = document.getElementById("price-range"),
    priceMin = document.getElementById("price-min"),
    priceMax = document.getElementById("price-max");

let lastMinPrice;
let lastMaxPrice; // Слайдер забирает цены при каждом движении и обновлял цену каждый такой шаг.
// В итоге страница перезагружалась слишком часто и вылетала ошибка
// Было решено просто брать последнюю цену и сверять с ценой, когда пользователь отпустил слайдер
function getCurrentURL() {
    return window.location.href
}

function changeMin(minPrice) {
    if (minPrice === lastMinPrice) {
        let url = new URL(getCurrentURL())
        url.searchParams.set('minPriceByUser', minPrice.match(/\d+/gm).join(''));
        window.location.href = url;
    } else {
        lastMinPrice = minPrice;
    }
}

function changeMax(maxPrice) {
    if (maxPrice === lastMaxPrice) {
        let url = new URL(getCurrentURL())
        url.searchParams.set('maxPriceByUser', maxPrice.match(/\d+/gm).join(''));
        window.location.href = url;
    } else {
        lastMaxPrice = maxPrice;
    }
}

function getMinPriceFromUrl() {
    let minimal;
    try {
        minimal = window.location.search.match(/minPriceByUser=\d+/)[0].match(/\d+/gm)[0];
    } catch (e) {
        minimal = priceMin.value
    }
    return minimal;
}

function getMaxPriceFromUrl() {
    let maximum;
    try {
        maximum = window.location.search.match(/maxPriceByUser=\d+/)[0].match(/\d+/gm)[0];
    } catch (e) {
        maximum = priceMax.value
    }
    return maximum;
}

//конец блока кода о фильтрации

//блок кода для создания слайдера

if (priceSlider != null) {
    noUiSlider.create(priceSlider, {
        start: [+getMinPriceFromUrl(), +getMaxPriceFromUrl()],
        connect: true,
        step: 1,
        range: {
            "min": +priceMin.value,
            "max": +priceMax.value
        },
        behaviour: 'drag-smooth-steps-tap',
        format: wNumb({
            decimals: 0,
            thousand: " ",
            suffix: " руб"
        })
    });

    priceSlider.noUiSlider.on("update", function (values, handle) {
        let value = values[handle];

        if (!handle) {
            priceMin.value = value;
            changeMin(value);
        } else {
            priceMax.value = value;
            changeMax(value);
        }
    });

    priceMin.addEventListener("change", function () {
        priceSlider.noUiSlider.set([this.value, null]);
        changeMin(this.value);
    });

    priceMax.addEventListener("change", function () {
        priceSlider.noUiSlider.set([null, this.value]);
        changeMax(this.value);
    });
}
//конец блока кода о создании слайдера
//ВЫШЕ ДЛЯ ФАЙЛА catalog-category

//блок кода для сортировки по возрастанию или убыванию цены

const idToOrders = {
        'order-price': 'price',
        'order-popularity': 'popularity',
        'order-sketchNumber': 'id',
        'order-percent': 'percent'
}
const ordersToId = {
        'price': 'order-price',
        'popularity': 'order-popularity',
        'id': 'order-sketchNumber',
        'percent': 'order-percent'
}
function getSearchParams() {
    return  new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
}
function getOrderScending() {
    return getSearchParams().orderScending
}
function getOrder() {
    return getSearchParams().order
}

function changeArrowIcon(order, orderScending) {
    const arrowId = ordersToId[order] + '-arrow'
    if (orderScending === 'desc') {
        document.getElementById(arrowId).style.display = 'inline';
        document.getElementById(arrowId).style.transform = 'rotate(180deg)';
    } else if (orderScending === 'asc') {
        document.getElementById(arrowId).style.display = 'inline';
    }
}
function changeOrderScendingSpanTitle(orderScending) {
    document.getElementById("order-scending-title-" + orderScending).style.display = 'inline';
}
function changeFilterIcon (order, orderScending) {
    const filterId = ordersToId[order] + '-filter'
    if (orderScending === 'desc') {
        document.getElementById(filterId+'-down').style.display = 'inline';
    } else if (orderScending === 'asc') {
        document.getElementById(filterId+'-up').style.display = 'inline';
    }
}
function paintOrderButtonInRed (order) {
    try {
        document.getElementById(order).style.backgroundColor = '#F5320E';
    } catch {
        return 0;
    }
}
function changeAppearanceDependsOnOrder() {
    const order = getOrder()
    const orderScending = getOrderScending()

    try{
        //for desktop
        changeArrowIcon(order, orderScending)

        //for mobile
        changeFilterIcon(order, orderScending)
        paintOrderButtonInRed(ordersToId[order])
        changeOrderScendingSpanTitle(orderScending)
    } catch (e) {
    }

}
if (document.getElementById('order-sketchNumber')) {
    changeAppearanceDependsOnOrder()
}
function orderByParameter(idOfElement) {
    const orderName = idToOrders[idOfElement]
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
    const url = new URL(getCurrentURL())
    if (params.order === orderName) {
        if (params.orderScending === 'asc') {
            url.searchParams.set('orderScending', 'desc')
        } else {
            url.searchParams.set('orderScending', 'asc')
        }
    }
    else {
        url.searchParams.set('order', orderName)
        url.searchParams.set('orderScending','asc')
    }
    window.location.href = url;
}

//блок кода для сортировки по возрастанию или убыванию цены закончен
/* VIEW MORE */
document.addEventListener('DOMContentLoaded', function () {
    const links1 = document.querySelectorAll('.view_more1');
    const links2 = document.querySelectorAll('.view_more2');
    let clickCounts = JSON.parse(localStorage.getItem('clickCounts')) || {};

    function handleClick(event) {
        event.preventDefault();
        const link = event.currentTarget;
        const clickCount = clickCounts[link.classList[0]] || 0;
        clickCounts[link.classList[0]] = clickCount + 1;
        localStorage.setItem('clickCounts', JSON.stringify(clickCounts));
        if (clickCount === 0) {
            link.textContent = 'Смотреть все';
        }
        if (clickCount === 1) {
            /*  link.textContent = link.dataset.secondClickText; */
            window.location.href = link.dataset.redirectUrl;
        }
    }

    function resetClickCounts() {
        clickCounts = {};
        localStorage.setItem('clickCounts', JSON.stringify(clickCounts));
    }

    resetClickCounts();

    links1.forEach(function (link) {
        link.addEventListener('click', handleClick);
    });

    links2.forEach(function (link) {
        link.addEventListener('click', handleClick);
    });
});

// //блок кода для быстрого просмотра и калькулятора в нем
// let width = 100;
// let height = 100;
// let isOpen = false;
// let isNitro = false;
// let priceForSquare = 1;
//
// function changeWidth(value) {
//         width = value;
//         changeQuickForms()
//     }
//
//     function changeHeight(value) {
//         height = value;
//         changeQuickForms()
//     }
//
//     function changeIsOpen(value) {
//         isOpen = value;
//         changeQuickForms()
//     }
//
//     function changeIsNitro(value) {
//         isNitro = value;
//         changeQuickForms()
//     }
//
//     function changePriceForSquare(value) {
//         priceForSquare = value;
//         changeQuickForms()
//     }
//
//     function changeCheckboxesByClass(className, isChecked) {
//         let items = document.getElementsByClassName(className)
//         for (let i = 0; i < items.length; i++) {
//             items[i].checked = isChecked;
//         }
//     }
//
//     function changeInputsByClass(className, value) {
//         let items = document.getElementsByClassName(className)
//         for (let i = 0; i < items.length; i++) {
//             items[i].value = value;
//         }
//     }
//
//     function changeSpanByClass(className, value) {
//         let items = document.getElementsByClassName(className)
//         for (let i = 0; i < items.length; i++) {
//             items[i].textContent = value;
//         }
//     }
//
//
//     function changeQuickForms() {
//         changeCheckboxesByClass('quick-view-nitro', isNitro)
//         changeCheckboxesByClass('quick-view-isopen', isOpen)
//         changeInputsByClass('quick-view-width', width)
//         changeInputsByClass('quick-view-height', height)
//         changeSpanByClass("quick-view-total", countTotal())
//     }
//
//     function countTotal() {
//         let total = (width / 100 * height / 100) * priceForSquare
//         if (isOpen) {
//             total += 1500
//         }
//         if (isNitro) {
//             total += 550
//         }
//         return total
//     }
//
// //конец блока кода о калькуляторе и быстром просмотре


//блок кода для перемещения с карточки фотки
function goToProduct(photoName) {
    const numberOfProduct = photoName.match(/\d-\d+/)[0]
    window.location.href = "/product/" + numberOfProduct
}
// конец блока кода о перемещении

/* DROPDOWN */

const dropdowns = document.querySelectorAll('.dropdown-wrapper');
const span = document.querySelector('span');

dropdowns.forEach((dd) => {
    const links = dd.querySelectorAll('.dropdown-list a');
    dd.addEventListener('click', function () {
        this.classList.toggle('is-active');
    });

    links.forEach((element) => {
        element.addEventListener('click', function (evt) {
            span.innerHTML = evt.currentTarget.textContent;
        });
    });
});

// блок кода для скрывания баннера когда ширина экрана как у смартфона ()
function getWidth() {
  return Math.max(
    document.body.scrollWidth,
    document.documentElement.scrollWidth,
    document.body.offsetWidth,
    document.documentElement.offsetWidth,
    document.documentElement.clientWidth
  );
}

if (getWidth() < 768){
    const element = document.getElementById("alert_modal");
    element.remove();
} else if(!sessionStorage.getItem("alertWasShown")) {
    let alertModal = new bootstrap.Modal(document.getElementById('alert_modal'));
        setTimeout(() => alertModal.show(), 1000*60*3);
       (function() {
    document.onmousemove = handleMouseMove;
    function handleMouseMove(event) {
        var eventDoc, doc, body;

        event = event || window.event; // IE-ism

        // If pageX/Y aren't available and clientX/Y are,
        // calculate pageX/Y - logic taken from jQuery.
        // (This is to support old IE)
        if (event.pageX == null && event.clientX != null) {
            eventDoc = (event.target && event.target.ownerDocument) || document;
            doc = eventDoc.documentElement;
            body = eventDoc.body;

            event.pageX = event.clientX +
              (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
              (doc && doc.clientLeft || body && body.clientLeft || 0);
            event.pageY = event.clientY +
              (doc && doc.scrollTop  || body && body.scrollTop  || 0) -
              (doc && doc.clientTop  || body && body.clientTop  || 0 );
        }
        if(event.clientY < 10) {
            alertModal.show();
            sessionStorage.setItem('alertWasShown', 'true')
        }
    }
})();
}

//блок кода для открывания модального окна при нажатии на кнопку купить
let buyViewModal = new bootstrap.Modal(document.getElementById('buy_view'));
    function buyViewHandler(id){
        const folderOfGrid = id.match(/\d+/gm)[0]
        const numberOfGrid = id.match(/\d+/gm)[1]
        document.getElementById('buy_view_path_folder').textContent = folderOfGrid;
        document.getElementById('buy_view_path_file').textContent = numberOfGrid;
        buyViewModal.show();
    }

//блок кода для быстрого просмотра и вызова модального окна
let width = 100;
let height = 100;
let isOpen = false;
let isNitro = false;
let priceForSquare = 1;

let quickViewModal = new bootstrap.Modal(document.getElementById('quick_view'));
    function quickViewHandler(id){
        const pathFolder = id.match(/\d+/gm)[0]
        const pathFile = id.match(/\d+/gm)[1]
        const price = id.match(/\d+/gm)[2]
        const salePrice = id.match(/\d+/gm)[3]
        changePriceForSquare(price)
        changeQuickViewWindow(pathFolder, pathFile, price, salePrice)
        changePictures(pathFolder, pathFile)
        quickViewModal.show(price, salePrice);
    }

    function changeQuickViewWindow(pathFolder, pathFile, price, salePrice){
        changeSpanTextById('product_quick_view-path_folder', pathFolder)
        changeSpanTextById('product_quick_view-path_file', pathFile)
        changeSpanTextById('product_quick_view-price', price)
        changeSpanTextById('product_quick_view-salePrice', salePrice)
    }
    function changeSpanTextById(spanId, value) {
        document.getElementById(spanId).textContent = value
    }
    function changeWidth(value) {
        width = value;
        countTotal()
    }

    function changeHeight(value) {
        height = value;
        countTotal()
    }

    function changeIsOpen(value) {
        isOpen = value;
        countTotal()
    }

    function changeIsNitro(value) {
        isNitro = value;
        countTotal()
    }

    function changePriceForSquare(value) {
        priceForSquare = value;
        countTotal()
    }

    function changePictures(pathFolder, pathFile) {
        const photoOfCarousel = document.getElementById('quick-view-carousel-picture')
        const photoOfCarouselF = document.getElementById('quick-view-carousel-picture-f')
        let srcOfPhotoStatic = photoOfCarousel.getAttribute('data-original')
        let srcOfPhotoStaticF = photoOfCarouselF.getAttribute('data-original')
        srcOfPhotoStatic = srcOfPhotoStatic + "/" + pathFolder + "/solid/" + pathFile + ".webp"
        srcOfPhotoStaticF = srcOfPhotoStaticF + "/" + pathFolder + "/solid/" + pathFile + " F.webp"
        photoOfCarousel.setAttribute('src', srcOfPhotoStatic)
        photoOfCarouselF.setAttribute('src', srcOfPhotoStaticF)
    }
    function countTotal() {
        let total = (width / 100 * height / 100) * priceForSquare
        if (isOpen) {
            total += 1500
        }
        if (isNitro) {
            total += 550
        }
        changeSpanTextById('quick-view-total', Math.round(total))
    }