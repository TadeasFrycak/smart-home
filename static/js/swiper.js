$(document).ready(function(){
  // ----------------------------------------------
  // All about Swiper
  // ----------------------------------------------

  var touchStart;
  var sliderMove = 0;
  var tap = 0;
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
    if (delta == 1) {
      swiper.slideNext();
    }
    else {
      swiper.slidePrev();
    }
});

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
