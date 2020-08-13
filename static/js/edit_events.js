/*
*
*   Eventy v editovacím módu
*
*/

$(document).ready(function(){
  $("body").on("click", "#save", function() {
    socketio.emit("save");
  });

  // Kliknutí na "přidat stránku" v Menu
  $("body").on("click", "#append-slide", function() {
    socketio.emit("slide_append");
  });

  $("body").on("click", "#prepend-slide", function() {
    socketio.emit("slide_prepend");
  });

  // Kliknutí na "Odebrat stránku" v Menu
  $("body").on("click", "#remove-slide", function() {
    let index = swiper.realIndex;

    socketio.emit("slide_delete", {"index": index});
  });

  $("body").on("click", "#move-slide-right", function() {
    let old_index = swiper.realIndex;
    let new_index = swiper.realIndex+1;
    if (swiper.slides.length !== new_index) {
      socketio.emit("slide_index", {"old_index": old_index, "new_index": new_index});
    }
  });

  $("body").on("click", "#move-slide-left", function() {
    let old_index = swiper.realIndex;
    let new_index = swiper.realIndex-1;
    if (new_index !== -1) {
      socketio.emit("slide_index", {"old_index": old_index, "new_index": new_index});
    }
  });
});
