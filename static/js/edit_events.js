/*
*
*   Events in edit mode
*
*/

$(document).ready(function(){
  $("body").on("click", ".save", function() {
    socketio.emit("save");
  });

  // Kliknutí na "přidat stránku" v Menu
  $("body").on("click", ".append-slide", function() {
    let index = swiper.realIndex;
    socketio.emit("slide_append", {"slide_index": index});
  });

  // Click on "Remove slide" in dropdown
  $("body").on("click", ".remove-slide", function() {
    let index = swiper.realIndex;
    socketio.emit("slide_delete", {"index": index});
  });

  $("body").on("click", ".move-slide-right", function() {
    let old_index = swiper.realIndex;
    let new_index = swiper.realIndex+1;
    if (swiper.slides.length !== new_index) {
      socketio.emit("slide_index", {"old_index": old_index, "new_index": new_index});
    }
    else {
      notify(_("Slide"), _("is already on the end!"), "warning", 2000);
    }
  });

  $("body").on("click", ".move-slide-left", function() {
    let old_index = swiper.realIndex;
    let new_index = swiper.realIndex-1;
    if (new_index !== -1) {
      socketio.emit("slide_index", {"old_index": old_index, "new_index": new_index});
    }
    else {
      notify(_("Slide"), _("is already on the beginning!"), "warning", 2000);
    }
  });
});
