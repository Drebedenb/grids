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

function getCurrentURL () {
  return window.location.href
}
function changeMin(minPrice) {
    console.log(minPrice);
    let url = new URL(getCurrentURL())
    url.searchParams.append('minPrice', minPrice);
    console.log(url)
    // window.location.href = url;
}

function changeMax(maxPrice) {
}

let priceSlider = document.getElementById("price-range"),
    priceMin = document.getElementById("price-min"),
    priceMax = document.getElementById("price-max");

if (priceSlider != null) {
    noUiSlider.create(priceSlider, {
        start: [+priceMin.value, +priceMax.value],
        connect: true,
        step: 1,
        range: {
            "min": +priceMin.value,
            "max": +priceMax.value
        },
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


/* VIEW MORE */
const link = document.querySelector('.view_more');
let clickCount = localStorage.getItem('clickCount') || 0;

link.addEventListener('click', function(event) {
  event.preventDefault();
  
  clickCount++;
  
  if (clickCount === 1) {
    link.textContent = 'Все отзывы';
  }
  
  if (clickCount === 2) {
    if (window.location.href !== 'https://www.google.com') {
      window.location.href = 'https://www.google.com';
      localStorage.setItem('clickCount', 0);
    }
  }
  
  localStorage.setItem('clickCount', clickCount);
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


