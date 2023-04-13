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
    slidesPerView: 1,
    slidesPerGroup: 1,
    spaceBetween: 20,
    navigation: {
        prevEl: "#features-swiper-control .btn-swiper-prev",
        nextEl: "#features-swiper-control .btn-swiper-next"
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
            slidesPerView: 4,
            slidesPerGroup: 4,
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
        minimal =  priceMin.value
    }
    return minimal;
}
function getMaxPriceFromUrl() {
    let maximum;
    try {
       maximum = window.location.search.match(/maxPriceByUser=\d+/)[0].match(/\d+/gm)[0];
    } catch (e) {
        maximum =  priceMax.value
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
            link.textContent = link.dataset.secondClickText;
            window.location.href = link.dataset.redirectUrl;
        }
        if (clickCount === 1) {
            link.textContent = link.dataset.secondClickText;
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


