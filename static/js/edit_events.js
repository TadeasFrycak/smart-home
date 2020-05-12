/*
*
*   Eventy v editovacím módu
*
*/

$(document).ready(function(){
  $("body").on("click", "#save", function(e) {
  $.post("/save", {}, function(result){});
  });

  // Kliknutí na "přidat stránku" v Menu
  $("body").on("click", "#append-slide", function(e) {
    appendNewSlide();
  });

  // Kliknutí na "Odebrat stránku" v Menu
  $("body").on("click", "#remove-slide", function() {
    var index = swiper.realIndex;

    if (index == 0) swiper.slideTo(index+1, 1000);
    else swiper.slideTo(index-1, 1000);

    setTimeout(() => {swiper.removeSlide(index);}, 1000);

    $.post("/delete_slide",
    {
      "index": index
    },
    function(result){});
  });
});


function appendNewSlide()
{
  $.post("/append_slide", {
  },
  function(result){
    var json = JSON.parse(result);
    swiper.appendSlide(json.slide);
    swiper.slideTo(swiper.slides.length, 1000);

    var isEditActive = $("body").attr("is_edit_active");
    
    if (isEditActive == "true")
    {
      $(".add_new_tile_element").hide().fadeIn(2000);
      $(".btn-exit-edit-mode").hide().fadeIn(2000);

      // Připnutí Hammer pro každé "+" tlačítko
      $(".swiper-slide-active .add_new_tile_element").each(function() {
        var $this = $(this);
        var hammer = new Hammer(this);
        initTileTap(hammer, $this,1);
      });
  
      var lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
      bindSortable(SortableTiles.length,lastSortablePage[lastSortablePage.length-1]);
    }
  });
}
