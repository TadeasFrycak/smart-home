$(document).ready(function(){
    // ----------------------------------------------
    // Initialise Swiper
    // ----------------------------------------------

    new Swiper(".swiper-container", {
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
});