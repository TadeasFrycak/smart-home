/*function beforeRefresh(slide=swiper.realIndex) {
  let tileID;
  if ($(document.body).hasClass("modal-open")) {
    tileID = store($(".modal-here"), "tile-id");
  }
  else {
    tileID = null;
  }
  if (store($(".swipe-body"), "index-change") === true) {
    socketio.emit("before_refresh", {"data": {"slide_index": slide, "edit": store($(document.body), "is-edit-active"),
        "tile_id": tileID}, "tab_id": sessionStorage.tabID, "slide_index_change": true})
  }
  else {
    socketio.emit("before_refresh", {"data": {"slide_index": slide, "edit": store($(document.body), "is-edit-active"),
        "tile_id": tileID}, "tab_id": sessionStorage.tabID, "slide_index_change": false})
  }

}*/

$(document).ready(function(){
  // ----------------------------------------------
  // All about Swiper
  // ----------------------------------------------

  // Initialise Swiper
  swiper = new Swiper(".swiper-container", {
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    threshold: "10",
    on: {
      slideChange: function () {
        socketio.emit("slide_change", {"slide_index": swiper.realIndex, "tab_id": sessionStorage.tabID});
      },
    }
  });

  swiper.slideTo(store($(".swipe-body"), "slide"), 0);

  // Events
  swiper.on("slideChange", function () {
    // updateSearchBar();
  })

  document.getElementById("swiper-pagination").addEventListener("wheel", event => {
    const delta = Math.sign(event.deltaY);
    if (delta === 1) {
      swiper.slideNext();
    }
    else {
      swiper.slidePrev();
    }
  });

  $(".swiper-unfocus-on-enter").keydown(function(event){
    event.keyCode===13 && $(this).blur();
  });
});