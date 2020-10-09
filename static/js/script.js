$(document).ready(function() {

    /* For the sticky navigation */
    $('.js--section-features').waypoint(function(direction) {
        if (direction == "down") {
            $('nav').addClass('sticky');
        } else {
            $('nav').removeClass('sticky');
        }
    }, {
        offset: '60px;'
    })

    /* Scroll on buttons */
    $('.js--scroll-to-kontakt').click(function () {
        $('html,body').animate({scrollTop: $('.js--section-kontakt').offset().top}, 1000);

    });

    /* Navigation scroll */

    $(function() {
        $('a[href*=#]:not([href=#])').click(function() {
            if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    });



    /* Animations on scroll */
    $('.js--wp-1').waypoint(function(direction) {
        $('.js--wp-1').addClass('animated fadeIn');
    }, {
        offset: '50%'
    });

    $('.js--wp-2').waypoint(function(direction) {
        $('.js--wp-2').addClass('animated pulse');
    }, {
        offset: '50%'
    });

    $('.js--wp-3').waypoint(function(direction) {
        $('.js--wp-3').addClass('animated shake');
    }, {
        offset: '50%'
    });


    /* Mobile nav */
    $(".js--nav-icon").click(function() {
        var nav = $(".main-nav");
        var icons = $(".js--nav-icon i");

        nav.slideToggle(200);
        if (icons.hasClass("fa-bars")) {
            icons.addClass("fa-times");
            icons.removeClass("fa-bars");
        } else {
            icons.addClass("fa-bars");
            icons.removeClass("fa-times");
        }

    });


});