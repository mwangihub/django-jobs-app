type = ['', 'info', 'success', 'warning', 'danger'];


class Creator {
    constructor(icon, message, title, href, alert) {
        this.icon = icon;
        this.message = message;
        this.title = title;
        this.href = href;
        this.alert = alert;
    }
    converter = key => {
        if (key != key.toLowerCase()) {
            key = key.replace(/[A-Z]/g, m => "-" + m.toLowerCase());
        }
        return key
    }
    createEl = obj => {
        let type = obj.type || 'div';
        let el = document.createElement(type);
        if (obj.attrs) {
            for (let key of(Object.keys(obj.attrs))) {
                let value = obj.attrs[key];
                el.setAttribute(this.converter(key), value);
            }
        }
        for (const key of(Object.keys(obj))) {
            if (key != 'attrs' && key != 'type') {
                el[key] = obj[key];
            }
        }
        return el;
    }
    notifyDiv = alert => {
        let color;
        if (alert === 'error') {
            color = 'danger'
        } else {
            color = alert
        }
        return {
            type: 'div',
            className: `alert__div alert alert-${color} animated fadeInDown`,
        }
    }

    dismissBtn = () => {
        return {
            type: 'i',
            className: 'close bi-x-square-fill',
            attrs: {
                onclick: "dismissFunc(this)",
            },
        }
    }
    spanIcon = icon => {
        return {
            type: 'i',
            className: `type__icon ${icon}`,
            style: "",
        }
    }
    spanTitle = title => {
        return {
            type: 'span',
            innerHTML: title,
            className: "title",
        }
    }
    spanMessage = message => {
        return {
            type: 'span',
            innerHTML: message,
        }
    }
    anchor = href => {
        return {
            type: 'a',
            href: href,
            className: "link_to",
        }
    }
}


notify = {
    showNotification: (m = '', x = '', a = '') => {
        let dismissibles = [];

        let create = new Creator;
        let iconName, title;
        if (x === 'error') {
            iconName = 'bi-exclamation-diamond-fill';
            title = 'Error message!';
        }
        if (x === 'warning') {
            iconName = 'bi-shield-fill-exclamation';
            title = 'Warning message!';
        }
        if (x === 'success') {
            iconName = 'bi-check-all';
            title = 'Success message';
        }
        if (x === 'info') {
            iconName = 'bi-info-circle-fill';
            title = 'Info message';
        }
        let root = document.querySelector('#notification');
        console.log(root);
        let div = create.createEl(create.notifyDiv(x));
        let dismissBtn = create.createEl(create.dismissBtn());
        let spanIcon = create.createEl(create.spanIcon(iconName));
        let spanTitle = create.createEl(create.spanTitle(title));
        let spanMessage = create.createEl(create.spanMessage(m));
        let anchor = create.createEl(create.anchor(a));
        anchor.appendChild(spanMessage);
        div.appendChild(dismissBtn);
        div.appendChild(spanIcon);
        div.appendChild(spanTitle);
        div.appendChild(anchor);
        root.appendChild(div);
        dismissibles.push(div);
        if (dismissibles.length) {
            setTimeout(function() {
                for (var i = 0; i < dismissibles.length; i++) {
                    if (dismissibles[i] === div) {
                        dismissibles[i].classList.add("fadeOutUp");
                        dismissibles.splice(i, 1);
                        setTimeout(() => {
                            div.remove();
                        }, 500);
                    }
                }
            }, 8000);
        }
    },
}


fn = {
    documentLoaded: (func) => {
        document.addEventListener('DOMContentLoaded', func);
    },
    /* CUSTOM METHODS */
    /* Easy selector helper function */
    select: (el, all = false) => {

        el = el.trim()

        if (all) {
            return [...document.querySelectorAll(el)]
        } else {
            return document.querySelector(el)
        }
    },

    /*Easy event listener function */
    on: (type, el, listener, all = false) => {
        let selectEl = fn.select(el, all)
        if (selectEl) {
            if (all) {
                selectEl.forEach(e => e.addEventListener(type, listener))
            } else {
                selectEl.addEventListener(type, listener)
            }
        }
    },

    carousel: (loopTime = 4000, waitReadTime = 8000) => {
        //   console.log('load');
        const slides = fn.select('.slide', true);
        const slider = fn.select('.slider');
        const buttons = fn.select('.buttons .bi', true);
        let timeOut = null,
            waitUntillRead;
        // function for getting next & Previous slides
        var getNextPrev = () => {
                const activeSlide = fn.select('.slide.active');
                const activeIndex = slides.indexOf(activeSlide);
                let next, prev;
                if (activeIndex === slides.length - 1) next = slides[0]
                else next = slides[activeIndex + 1];
                if (activeIndex === 0) prev = slides[slides.length - 1]
                else prev = slides[activeIndex - 1];
                return [next, prev];
            }
            // 
        var getPosition = () => {
            const activeSlide = fn.select('.slide.active');
            const activeIndex = slides.indexOf(activeSlide);
            const [next, prev] = getNextPrev();
            slides.forEach((el, i) => {
                if (i === activeIndex) el.style.transform = 'translateX(0)';
                else if (el === prev) el.style.transform = 'translateX(-100%)';
                else if (el === next) el.style.transform = 'translateX(100%)';
                else el.style.transform = 'translate(100%)';
                el.addEventListener('transitionend', e => {
                    el.classList.remove('top')
                })
            });
        }
        const nextSlide = (o) => {
            clearTimeout(timeOut);
            const current = fn.select('.slide.active');
            const [next, prev] = getNextPrev();
            if (current.classList.contains('top')) return;
            current.classList.remove('active');
            current.classList.add('top');
            next.classList.add('top');
            current.style.transform = 'translate(-100%)';
            next.style.transform = 'translate(0)';
            next.classList.add('active');
            getPosition();
            getActiveDot();
            autoCarousel();
        };
        const previousSlide = (o) => {
            clearTimeout(timeOut);
            const current = fn.select('.slide.active');
            const [next, prev] = getNextPrev();
            if (current.classList.contains('top')) return;
            current.classList.remove('active');
            current.classList.add('top');
            prev.classList.add('top');
            current.style.transform = 'translate(100%)';
            prev.style.transform = 'translateX(0)';
            prev.classList.add('active');
            getPosition();
            getActiveDot();
            autoCarousel(true);
        };
        fn.on('click', '.buttons .bi', el => {
            let e = el.target;
            if (e.classList.contains('bi-arrow-right-circle')) nextSlide(e);
            else if (e.classList.contains('bi-arrow-left-circle')) previousSlide(e);
        }, true);

        slides.forEach(el => {
            let e = el.firstElementChild.firstElementChild.childNodes[1];
            let style = e.classList
            let content = e.innerHTML.trim()
            const dotEl = fn.select('.courosel__body .indicator');
            const dot = document.createElement('div');
            dot.classList.add('dot');
            const p = document.createElement('p');
            const s = document.createElement('span');
            p.classList.add('indicate');
            // style.forEach(style => {
            //     dot.classList.add(style);
            // });
            p.innerHTML = content;
            dot.appendChild(p);
            dot.appendChild(s);
            dotEl.appendChild(dot);
        });
        const getActiveDot = () => {
            const activeSlide = fn.select('.slide.active');
            const activeIndex = slides.indexOf(activeSlide);
            const allDts = fn.select('.courosel__body .indicator .dot', true);
            allDts.forEach(el => {
                el.classList.remove('active');
            });
            allDts[activeIndex].classList.add('active');
        }
        fn.select('.courosel__body .indicator .dot', true).forEach((e, i) => {
            e.addEventListener('click', (el) => {
                (function clearTimer() {
                    clearTimeout(timeOut);
                    clearTimeout(waitUntillRead);
                    timeOut = null;
                })();
                const [next, prev] = getNextPrev();
                let e = el.target;
                let leftDirection = false;
                slides.forEach(slide => {
                    slide.classList.remove('active');
                });
                if (slides[i].classList.contains('top')) {
                    slides[i].classList.remove('top');
                } else {
                    slides[i].classList.add('top');
                }
                slides[i].classList.add('active');
                //  slides[i].classList.add('top');
                getPosition();
                getActiveDot();
                if (timeOut === null) {
                    if (slides[i] === next) leftDirection = false;
                    else if (slides[i] === prev) leftDirection = true;
                    else if (slides[i] !== prev && slides[i] !== next) leftDirection = false;
                    else leftDirection = true;
                    waitUntillRead = setTimeout(() => {
                        autoCarousel(leftDirection);
                    }, waitReadTime);
                }
            });
        });


        function autoCarousel(left = false) {
            clearTimeout(waitUntillRead);
            timeOut = setTimeout(() => {
                if (left) previousSlide();
                else nextSlide();
            }, loopTime);
        }
        autoCarousel(false);
        getActiveDot();
    },


    initGoogleMaps: function() {
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
            zoom: 13,
            center: myLatlng,
            scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
            styles: [{ "featureType": "water", "stylers": [{ "saturation": 43 }, { "lightness": -11 }, { "hue": "#0088ff" }] }, { "featureType": "road", "elementType": "geometry.fill", "stylers": [{ "hue": "#ff0000" }, { "saturation": -100 }, { "lightness": 99 }] }, { "featureType": "road", "elementType": "geometry.stroke", "stylers": [{ "color": "#808080" }, { "lightness": 54 }] }, { "featureType": "landscape.man_made", "elementType": "geometry.fill", "stylers": [{ "color": "#ece2d9" }] }, { "featureType": "poi.park", "elementType": "geometry.fill", "stylers": [{ "color": "#ccdca1" }] }, { "featureType": "road", "elementType": "labels.text.fill", "stylers": [{ "color": "#767676" }] }, { "featureType": "road", "elementType": "labels.text.stroke", "stylers": [{ "color": "#ffffff" }] }, { "featureType": "poi", "stylers": [{ "visibility": "off" }] }, { "featureType": "landscape.natural", "elementType": "geometry.fill", "stylers": [{ "visibility": "on" }, { "color": "#b8cb93" }] }, { "featureType": "poi.park", "stylers": [{ "visibility": "on" }] }, { "featureType": "poi.sports_complex", "stylers": [{ "visibility": "on" }] }, { "featureType": "poi.medical", "stylers": [{ "visibility": "on" }] }, { "featureType": "poi.business", "stylers": [{ "visibility": "simplified" }] }]

        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title: "Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },

}