$(document).ready(function(){
  // ----------------------------------------------
  // Global events
  // ----------------------------------------------

  ADD_TILE = "<div class='tile_ghost_prefab_class tile' data-id='id-add'style='display: inline-block; box-shadow: none; background-color:transparent'><img class='' src='/static/images/static/add.png' style='width:30px; position:relative; transform: translate(-50%,-50%); left:30%; top:50%; cursor: pointer;'></div>";
  SortableTiles = [];


  // Bootstrap dropdown
  $(".dropdown").on("show.bs.dropdown", function(e){
    $(this).find(".dropdown-menu").slideDown();
  });

  $(".dropdown").on("hide.bs.dropdown", function(e){
    e.preventDefault();
    $(this).find(".dropdown-menu").first().stop(true, true).slideUp(400, function(){
      $(".dropdown").removeClass("show");
      $(".dropdown-menu").removeClass("show");
      $(".dropdown").find(".dropdown-toggle").attr("aria-expanded","false");
    });
  });

  $("body").on("click", "#edit-page", function(e) {
    activateEdit(false);
  });

  // Button exit edit mode
  $("body").on("click", ".btn-exit-edit-mode", function(e) {
    exitEditMode();
  });

  $("body").on("click", "#shutdown", function(e) {
    window.location.href = "/shutdown"
  });
  $("body").on("click", "#restart", function(e) {
    $.post("/restart", {});

    setTimeout(() => {$.post("/reload", {});}, 2000);
    setTimeout(() => {location.reload();}, 2500);
  });
});

function activateEdit(reactivate)
{
  if (editMode === true) {
    for (var i = 0; i < SortableTiles.length; i++) {
      SortableTiles[i].destroy();
    }
    exitEditMode();
  }

  else if (editMode === false) {
    // Aktivuje edit mod

    var SortablePages = document.getElementsByClassName("c_sortable_page_grid");
    
    for (var i = 0; i < SortablePages.length; i++)
    {
      bindSortable(i,SortablePages[i])
    }

    editMode = true;
    swiper.allowTouchMove = false;

    $(".tile_ghost_prefab_class").remove();

    $(".zoomable").append(ADD_TILE);
    $(".swiper-slide").append("<button type='button' class='btn btn-outline-info btn-exit-edit-mode'>Ukončit upravovací mód</button>");



    // TODO: DUPLIKUJí se!
    if (reactivate == false)
    {
      $(".btn-exit-edit-mode").hide().fadeIn(2000);
      // $(".btn-exit-edit-mode").remove().fadeIn(2000);
      $(".tile_ghost_prefab_class").hide().fadeIn(2000);
      $(".bcg-image").fadeIn(2000);
    }

    $(".tile_ghost_prefab_class").each(function() {
      var $this = $(this);
      console.log($this);
      var hammer = new Hammer(this);
      initTilePress(hammer, $this,1);
    });


    setTimeout(() => {$("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>Ukončit upravovací mód</a>");}, 300);
  }
}

// Functions
function exitEditMode(){
  editMode = false;
  swiper.allowTouchMove = true;
  $(".tile_ghost_prefab_class").show().fadeOut(2000);
  $(".btn-exit-edit-mode").show().fadeOut(2000);
  $(".bcg-image").fadeOut(2000);
  setTimeout(() => {$("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>Upravit tuto stránku</a>");}, 300);
}

function bindEventToTile()
{
  
}

function bindSortable(index,item)
{
  SortableTiles[index] = Sortable.create(item, {
    animation: 150,
    swapThreshold: 1,
    ghostClass: "tile-sortable-move",

    onUpdate: function (/**Event*/evt) {
      $.post("/tile_index_rwr", {
        "slide": swiper.realIndex,
        "old_index": evt.oldIndex,
        "new_index": evt.newIndex
        });
      console.log("Slide: " + swiper.realIndex);
      console.log("Old index: " + evt.oldIndex);
      console.log("New index: " + evt.newIndex);
    },  
  });
}