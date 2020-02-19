$(document).ready(function(){
    // ----------------------------------------------
    // Initialise Swiper
    // ----------------------------------------------
    var touch_start;
    var tap = 0;
    var slider_move = 0;
    mySwiper = new Swiper(".swiper-container", {
        pagination: {
            el: ".swiper-pagination",
            dynamicBullets: true,
            },
        threshold: "10"
        // allowTouchMove: false,
        // simulateTouch: false,
        // touchStartPreventDefault: true,
        // noSwiping: true,
        // noSwipingClass = "swiper-no-swiping"
        });

    mySwiper.on("touchStart", function(event) {
        touch_start = event.layerX
        });

    mySwiper.on("tap", function() {
        tap = 1;
        });

    mySwiper.on("touchEnd", function(event) {
        if (tap === 0 && slider_move === 0 && is_edit === true && Math.abs(touch_start-event.layerX) > 200) {
            $.notify({
                title: "<strong>Swipování není povoleno!</strong>",
                message: "Nelze swipovat, dokud je aktivní editační mód!"
            }, {
                type: "warning",
                delay: 5000,
                mouse_over: "pause",
                allow_dismiss: true,
                animate: {
                    enter: "animated fadeInRight",
                    exit: "animated fadeOutRight"
                },
                z_index: 2000
            });
            }
        tap = 0;
        slider_move = 0;
        });

    mySwiper.on("sliderMove", function() {
            slider_move = 1;
        });
});