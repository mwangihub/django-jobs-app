(function() {
    "use strict";

    /**
     * Easy selector helper function
     */
    const select = (el, all = false) => {
        el = el.trim()
        if (all) {
            return [...document.querySelectorAll(el)]
        } else {
            return document.querySelector(el)
        }
    }

    /**
     * Easy event listener function
     */
    const on = (type, el, listener, all = false) => {
        let selectEl = select(el, all)
        if (selectEl) {
            if (all) {
                selectEl.forEach(e => e.addEventListener(type, listener))
            } else {
                selectEl.addEventListener(type, listener)
            }
        }
    }

    /**
     * Easy on scroll event listener 
     */
    const onscroll = (el, listener) => {
        el.addEventListener('scroll', listener)
    }

    /**
     * LOGIN AND SIGNUP MODALS
     */
    on('click', '#login__btn', function(e) {
        select('#login__modal').style.display = "block";
        select('#signup__modal').style.display = "none";
    }, true)

    on('click', '#signup__btn', function(e) {
        select('#login__modal').style.display = "none";
        select('#signup__modal').style.display = "block";
    }, true)
    on('click', '#login__close', function(e) {
        select('#login__modal').style.display = "none";
    })

    on('click', '#signup__close', function(e) {
        select('#signup__modal').style.display = "none";
    })

    document.onclick = function(event) {

            if (event.target == select('#login__modal')) {
                select('#login__modal').style.display = "none";
            }
            if (event.target == select('#signup__modal')) {
                select('#signup__modal').style.display = "none";
            }


        }
        /**
         * Navbar links active state on scroll
         */
    let navbarlinks = select('#navbar .scrollto', true)
    const navbarlinksActive = () => {
        let position = window.scrollY + 200
        navbarlinks.forEach(navbarlink => {
            if (!navbarlink.hash) return
            let section = select(navbarlink.hash)
            if (!section) return
            if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
                navbarlink.classList.add('active')
            } else {
                navbarlink.classList.remove('active')
            }
        })
    }
    window.addEventListener('load', navbarlinksActive)
    onscroll(document, navbarlinksActive)


    var mql = window.matchMedia('(max-width: 600px)');

    function screenTest(e) {
        if (e.matches) {
            /* the viewport is 600 pixels wide or less */
            console.log('Remove doms');

        } else {
            console.log("pass");
        }
    }

    mql.addEventListener('change', screenTest);

    /**
     * Scrolls to an element with header offset
     */
    const scrollto = (el) => {
        let header = select('#header')
        let offset = header.offsetHeight

        let elementPos = select(el).offsetTop
        window.scrollTo({
            top: elementPos - offset,
            behavior: 'smooth'
        })
    }

    /**
     * Toggle .header-scrolled class to #header when page is scrolled
     */
    let selectHeader = select('#header')
    if (selectHeader) {
        const headerScrolled = () => {
            if (window.scrollY > 100) {
                selectHeader.classList.add('header-scrolled')
            } else {
                selectHeader.classList.remove('header-scrolled')
            }
        }
        window.addEventListener('load', headerScrolled)
        onscroll(document, headerScrolled)
    }

    /**
     * Back to top button
     */
    let backtotop = select('.back-to-top')
    if (backtotop) {
        const toggleBacktotop = () => {
            if (window.scrollY > 100) {
                backtotop.classList.add('active')
            } else {
                backtotop.classList.remove('active')
            }
        }
        window.addEventListener('load', toggleBacktotop)
        onscroll(document, toggleBacktotop)
    }

    /**
     * Mobile nav toggle
     */
    on('click', '.mobile-nav-toggle', function(e) {
        select('#navbar').classList.toggle('fadeInLeft')
        select('#navbar').classList.toggle('navbar-mobile')
        this.classList.toggle('bi-grid-3x3-gap-fill')
        this.classList.toggle('bi-x-square-fill')
    });

    on('click', '.cover__mobile-nav', function(e) {
        select('.nav-masthead').classList.toggle('cover__navbar-mobile')
        this.classList.toggle('bi-grid-3x3-gap-fill')
        this.classList.toggle('bi-x-square-fill')
    });

    const userMenu = e => {
        this.classList.toggle('notify')
        let el = select('.action__wrapper');
        if (el.classList.contains('innactive')) {
            el.classList.remove('innactive');
            el.classList.remove('fadeOutUp');
            el.classList.add('fadeInDown');
            el.classList.add('active');
        } else if (el.classList.contains('active')) {
            el.classList.remove('active');
            el.classList.remove('fadeInDown');
            el.classList.add('fadeOutUp');
            setTimeout(() => {
                el.classList.add('innactive');
            }, 1000)
        }
    }
    on('click', '.user__actions .link', function(e) {
        console.log(this);
        let el = select('.action__wrapper');
        if (el.classList.contains('innactive')) {
            el.classList.remove('innactive');
            el.classList.remove('fadeOutUp');
            el.classList.add('fadeInDown');
            el.classList.add('active');
            this.classList.add('notify');

        } else if (el.classList.contains('active')) {
            this.classList.remove('notify');

            el.classList.remove('active');
            el.classList.remove('fadeInDown');
            el.classList.add('fadeOutUp');
            setTimeout(() => {
                el.classList.add('innactive');
            }, 1000)
        }
    });


    /**
     * Mobile nav dropdowns activate
     */
    on('click', '.navbar .dropdown > a', function(e) {
        if (select('#navbar').classList.contains('navbar-mobile')) {
            e.preventDefault()
            this.nextElementSibling.classList.toggle('dropdown-active')
        }
    }, true)

    /**
     * Scrool with ofset on links with a class name .scrollto
     */
    on('click', '.scrollto', function(e) {
        if (select(this.hash)) {
            e.preventDefault()

            let navbar = select('#navbar')
            if (navbar.classList.contains('navbar-mobile')) {
                navbar.classList.remove('navbar-mobile')
                let navbarToggle = select('.mobile-nav-toggle')
                navbarToggle.classList.toggle('bi-list')
                navbarToggle.classList.toggle('bi-x')
            }
            scrollto(this.hash)
        }
    }, true)

    /**
     * Scroll with ofset on page load with hash links in the url
     */
    window.addEventListener('load', () => {
        if (window.location.hash) {
            if (select(window.location.hash)) {
                scrollto(window.location.hash)
            }
        }
    });

    /**
     * Preloader
     */
    let preloader = select('#preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            preloader.remove()
        });
    }

    /**
     * Porfolio isotope and filter
     */
    window.addEventListener('load', () => {
        let portfolioContainer = select('.portfolio-container');
        if (portfolioContainer) {
            let portfolioIsotope = new Isotope(portfolioContainer, {
                itemSelector: '.portfolio-item'
            });

            let portfolioFilters = select('#portfolio-flters li', true);

            on('click', '#portfolio-flters li', function(e) {
                e.preventDefault();
                portfolioFilters.forEach(function(el) {
                    el.classList.remove('filter-active');
                });
                this.classList.add('filter-active');

                portfolioIsotope.arrange({
                    filter: this.getAttribute('data-filter')
                });

            }, true);
        }

    });
    // Side menu
    // on('click', '.nav-item.active', function(e) {
    //     this.children[1].onclick = e => {
    //         e.stopPropagation();
    //     }
    // }, true);

    // for (let el of select('.nav-item', true)) {
    //     el.onclick = e => {
    //         if (el.classList.contains('active'))
    //             el.classList.remove('active')
    //         else el.classList.add('active')
    //     }
    // };
    for (let el of select('.menu_item', true)) {
        el.onclick = e => {
            //header
            if (el.classList.contains('active'))
                el.classList.remove('active')
            else el.classList.add('active')
        }
    };



})()