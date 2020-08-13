$(document).ready(function(){
  // ----------------------------------------------
  // All about Swiper
  // ----------------------------------------------

  let touchStart;
  let sliderMove = 0;
  let tap = 0;
  try {
  // Initialise Swiper
  swiper = new Swiper(".swiper-container", {
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    threshold: "10"
   });

  // Events
  swiper.on("tap", function() {
    tap = 1;
  });

  swiper.on("sliderMove", function() {
    sliderMove = 1;
  });

  swiper.on("touchStart", function(event) {
    touchStart = event.layerX
  });

  document.getElementById("swiper-pagination").addEventListener("wheel", event => {
    const delta = Math.sign(event.deltaY);
    if (delta === 1) {
      swiper.slideNext();
    }
    else {
      swiper.slidePrev();
    }
  });

  document.onkeydown = function(e) {
    switch(e.which) {
        case 37: // left
            swiper.slidePrev();
            break;

        case 38: // up
            if ($("body").hasClass("modal-open")) $("#myModal").animate({scrollTop: 0}, "slow");
            else $("html, body").animate({scrollTop: 0}, "slow");
            break;

        case 39: // right
            swiper.slideNext();
            break;

        case 40: // down
            if ($("body").hasClass("modal-open")) $("#myModal").animate({scrollTop: $(".modal-dialog").height()}, "slow");
            else $("html, body").animate({scrollTop: $(document).height()}, "slow");
            break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
};
  swiper.on("touchEnd", function(event) {
    // If user swiped
    if (tap === 0 && sliderMove === 0 && editMode === true && Math.abs(touchStart-event.layerX) > 300) {
      // Send local notification
      //$.notify({
      //  title: "<strong>Swipování není povoleno!</strong>",
      //  message: "Nelze swipovat, dokud je aktivní editační mód!"
      //}, {
      //  type: "warning",
      //  delay: 5000,
      //  mouse_over: "pause",
      //  allow_dismiss: true,
      //  animate: {
      //    enter: "animated fadeInRight",
      //    exit: "animated fadeOutRight"
      //  },
      //  z_index: 2000
      //});
    }

    tap = 0;
    sliderMove = 0;
  });
} catch {};  // Kvůli register a login
});
