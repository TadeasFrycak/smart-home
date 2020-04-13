$(document).ready(function(){
  $("body").on("click", "#append-slide", function(e) {
    // swiper.appendSlide("<div class='swiper-slide'> <div class='dropdown'> <img src='/static/images/static/settings-icon.png' class='page_settings_icon' data-toggle='dropdown'> <div class='dropdown-menu' aria-labelledby='dropdownMenuButton'> <a class='dropdown-item' id='edit-page'>Upravit tuto stránku</a> <a class='dropdown-item' id='append-slide'>Přidat novou stránku</a> <a class='dropdown-item' id='remove-slide'>Odebrat tuto stránku</a> <a class='dropdown-item'>Nastavení</a> </div> </div> <div class='swipe-header'> Bez názvu </div> <div class='swipe-content'> <div class='zoomable' style='display:inline-block;'>  </div> <div class='end-block'></div> </div></div>");    
    $.post("/append_slide", {},
    function(result){
      // swiper.appendSlide("<div class='swiper-slide'> <div class='dropdown'> <img src='/static/images/static/settings-icon.png' class='page_settings_icon' data-toggle='dropdown'> <div class='dropdown-menu' aria-labelledby='dropdownMenuButton'> <a class='dropdown-item' id='edit-page'>Upravit tuto stránku</a> <a class='dropdown-item' id='append-slide'>Přidat novou stránku</a> <a class='dropdown-item' id='remove-slide'>Odebrat tuto stránku</a> <a class='dropdown-item'>Nastavení</a> </div> </div> <div class='swipe-header'> Bez názvu </div> <div class='swipe-content'> <div class='zoomable' style='display:inline-block;'>  </div> <div class='end-block'></div> </div></div>");    
      // console.log(result);
      var json = JSON.parse(result);
      console.log(result);
      swiper.appendSlide(json.slide);
      swiper.slideTo(swiper.slides.length, 1000);
      
      if (editMode == true)
      {
        $(".swiper-slide-active .zoomable").append(ADD_TILE);
        $(".swiper-slide-active .tile_ghost_prefab_class").each(function() {
          var $this = $(this);
          console.log($this);
          var hammer = new Hammer(this);
          initTilePress(hammer, $this,1);
        });
    
        var lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
        bindSortable(SortableTiles.length,lastSortablePage[lastSortablePage.length-1]);
      }
    });


    
  });

  $("body").on("click", "#remove-slide", function(e) {
    var index = swiper.realIndex;

    if (index == 0) {
      console.log("ahoj");
      swiper.slideTo(index+1, 1000);
    }

    else {
      swiper.slideTo(index-1, 1000);
    }

    setTimeout(() => {swiper.removeSlide(index);}, 1000);

    $.post("/remove_slide",
            {
                "index": index
            },
            function(result){});
  });
});
