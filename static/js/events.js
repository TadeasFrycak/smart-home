/*
*
*   Globální eventy, pro needitovací část
*
*/
$(document).ready(function(){
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
    var current_edit_status = $("body").attr("is_edit_active");
    //DEBUG.logDebug("Current edit status: " + current_edit_status);
    if (current_edit_status == "false") changePageToEdit();
    if (current_edit_status == "true") changePageToNormal();
  });

  // Button exit edit mode
  $("body").on("click", ".exit-edit-mode-button", function(e) {
    changePageToNormal();
  });

  $("body").on("click", "#settings", function(e) {
    // Request modal - Normal / Edit
    $.post("/get_modal_settings", 
    {}, 
    function(result){
      // ( > events.js )
      displaySettingsModal(result);
      $(".modal-edit-select-bcg").each(function() {
        var attr = $(this).attr('checked');
        if (typeof attr !== typeof undefined && attr !== false) {
          $(this).css({"border": "2px solid rgb(23, 162, 184)"});
        }
        Hammer(this).on("tap", function(elem) {
          // ( > modal_edit_events.js )
          modalEditPreviewImageTap(elem);
        });
  });
    });
  });

  $("body").on("click", "#shutdown", function(e) {
    window.location.href = "/shutdown"
  });

  $("body").on("click", "#restart", function(e) {
    $.post("/restart", {});

    //setTimeout(() => {$.post("/reload", {});}, 2000);
  });

});

function displaySettingsModal(result){
  var json = JSON.parse(result);

  $(".modal-settings").empty();
  $(".modal-settings").append(json.modal);

  $("#mySettingsModal").modal({ keyboard: true })

  // Event při zavření modalu
  $("#mySettingsModal").on("hidden.bs.modal", function () {
    // $(".swipe-body").css({"filter": "none", "transition": "filter 0.5s"});
    // $(".bcg-real").css({"filter": "none", "transition": "filter 0.5s"});
    // $(".bcg-image").css({"filter": "none", "transition": "filter 0.5s"});
  })

  var settingsSwiper = new Swiper('.settingSwiper', {
    slidesPerView: 4,
    spaceBetween: 30,
    centeredSlides: true,
    // pagination: {
    //   el: '.settingsSwiperPagination',
    //   clickable: true,
    // },
    // navigation: {
    //   nextEl: '.swiper-button-next',
    //   prevEl: '.swiper-button-prev',
    // },
  });

}

// Po doteku na Toggle tlačítko ( < init.js )
function tappedOnToggle($this)
{
  var isEditActive = $("body").attr("is_edit_active");

  if (isEditActive == "false")
    {
      $this.parent().toggleClass("tileActive");
      var tileID = $this.parent().attr("data-id");
      var tileState = $this.parent().find(".tileStatus").text().toLowerCase() == "on" ? 1 : 0;

      if (tileState === 1) {
        tileState = 0;
        $this.parent().find(".tileStatus").text("Off");
        //$this.parent().css("opacity", 0.7);
        // TODO NASTAVENÍ
        //$this.parent().css({"-moz-transform": "scale(1)", "-webkit-transform": "scale(1)", "transform": "scale(1)"})
        $this.parent().find(".toggle-dot").css("background-color", "rgba(255, 0, 0, 0.28)");
      }

      else if (tileState === 0) {
        tileState = 1;
        $this.parent().find(".tileStatus").text("On");
        //$this.parent().css("opacity", 1);
        // TODO NASTAVENÍ
        //$this.parent().css({"-moz-transform": "scale(1.03)", "-webkit-transform": "scale(1.03)", "transform": "scale(1.03)"})
        $this.parent().find(".toggle-dot").css("background-color", "rgba(0, 196, 42, 0.28)");
      }

      $.post("/tile", {
        "id": tileID,
        "value": tileState
      }
    );
  }
}

// add_new_tile_element

function changePageToNormal()
{
  $("body").attr("is_edit_active",false);
  swiper.allowTouchMove = true;
  $(".add_new_tile_element").show().fadeOut(2000);
  $(".exit-edit-mode-button").show().fadeOut(2000);
  $(".bcg-image").fadeOut(2000);
  setTimeout(() => {
    $("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>Upravit tuto stránku</a>");
    $(".dropdown-wrapper[dissapear-on-edit]").each(function() {
      $( this ).css("display","none");
    });
  }, 400);
  // TODO: smazat
  editMode = false;
  destroySortable();
  
  $(".swipe-header-textbox").each(function() {
    $( this ).prop("readonly",true)
    // $( this ).css({"border-bottom-width":"0px","border-bottom-style":"none","width":"fit-content"});
  });
}

function changePageToEdit()
{
  $("body").attr("is_edit_active",true);

  var SortablePages = document.getElementsByClassName("c_sortable_page_grid");
  
  // Vytvoří sortable položky 
  for (var i = 0; i < SortablePages.length; i++) bindSortable(i,SortablePages[i])
  
  // TODO: smazat
  editMode = true;

  swiper.allowTouchMove = false;

  $(".add_new_tile_element").hide().fadeIn(2000);
  $(".exit-edit-mode-button").hide().fadeIn(2000);
  $(".bcg-image").fadeIn(2000);

  // Přidělí každému "+" tlačítko Hammer
  $(".add_new_tile_element").each(function() {
    var $this = $(this);
    var hammer = new Hammer(this);
    initTileTap(hammer, $this,1);
  });

  setTimeout(() => {
    $("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>Ukončit upravovací mód</a>");
    $(".dropdown-wrapper[dissapear-on-edit]").each(function() {
      $( this ).css("display","block");
    });
  }, 400);

  $(".swipe-header-textbox").each(function() {
    $( this ).prop("readonly",false)
    // $( this ).css({"border-bottom-width":"1px","border-bottom-style":"solid","width":"fit-content"});
  });
  
}

// Zničí veškeré Srotable Itemy
// TODO: nefunguje
function destroySortable()
{
  for (var i = 0; i < SortableTiles.length; i++) {
    SortableTiles[i].destroy();
  }
}

// Vytvoří Sortable Itemy
function bindSortable(index,item)
{
  SortableTiles[index] = Sortable.create(item, {
    animation: 150,
    swapThreshold: 1,
    ghostClass: "tile-sortable-move",

    onUpdate: function (evt) {
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





