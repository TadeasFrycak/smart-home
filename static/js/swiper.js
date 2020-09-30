function beforeRefresh(slide=swiper.realIndex) {
  // TODO in new version remove this
  // let tileID = ""
  // if ($("body").hasClass("modal-open")) {
  //   tileID += "?" + $(".modal-here").attr("id_of_caller");
  // }
  // if ($("body").attr("data-is-edit-active") === "true") {
  //   if (swiper.realIndex === 0) {
  //     window.history.pushState("", "", "/edit" + tileID);
  //   }
  //   else {
  //     window.history.pushState("", "", "/edit/" + swiper.realIndex + tileID);
  //   }
  // }
  // else {
  //   if (swiper.realIndex === 0) {
  //     window.history.pushState("", "", "/" + tileID);
  //   }
  //   else {
  //     window.history.pushState("", "", "/" + swiper.realIndex + tileID);
  //   }
  // }

  let tileID;
  if ($("body").hasClass("modal-open")) {
    tileID = $(".modal-here").attr("id_of_caller");
  }
  else {
    tileID = null;
  }
  if ($(".swipe-body").data("index-change") === true) {
    socketio.emit("before_refresh", {"data": {"slide_index": slide, "edit": $("body").attr("data-is-edit-active"),
        "tile_id": tileID}, "tab_id": sessionStorage.tabID, "slide_index_change": true})
  }
  else {
    socketio.emit("before_refresh", {"data": {"slide_index": slide, "edit": $("body").attr("data-is-edit-active"),
        "tile_id": tileID}, "tab_id": sessionStorage.tabID, "slide_index_change": false})
  }

}

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
    threshold: "10"
  });

  swiper.slideTo($(".swipe-body").data("start-index"), 0);

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
});