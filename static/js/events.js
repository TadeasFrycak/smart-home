/*
*
*   Globální eventy, pro needitovací část
*
*/
$(document).ready(function(){
  SortableTiles = [];

  // Bootstrap dropdown
  $(".dropdown").on("show.bs.dropdown", function(){
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

  $("body").on("click", "#edit-page", function() {
    let current_edit_status = $("body").attr("is_edit_active");
    //DEBUG.logDebug("Current edit status: " + current_edit_status);
    if (current_edit_status === "false") changePageToEdit();
    if (current_edit_status === "true") changePageToNormal();
  });

  // Button exit edit mode
  $("body").on("click", ".exit-edit-mode-button", function() {
    changePageToNormal();
  });

  $("body").on("click", "#settings", function() {
    // Request modal - Normal / Edit
    console.log("Requested settings");
    socketio.emit("get_settings_modal");
  });

  $("body").on("click", "#shutdown", function() {
    $.post("/shutdown", {});
  });

  $("body").on("click", "#reload", function() {
    $.post("/reload", {});
  });

  $("body").on("click", "#restart", function() {
    $.post("/restart", {});

    //setTimeout(() => {$.post("/reload", {});}, 2000);
  });

  $('#myModal').on('hidden.bs.modal', function () {
    let element = document.querySelector(".slider input[type='range']")
    element.rangeSlider.destroy();
  })
});

function displaySettingsModal(result){
  // var json = JSON.parse(result);

  $(".modal-settings").empty().append(result.modal);
  $("#mySettingsModal").modal({ keyboard: true })

  $( ".modal-settings-page-appearance" ).click(function() {
    let change_to = $(this).attr("data-type");
    socketio.emit("user_change_mode", {"mode": change_to});
    console.log( "Change appearance to " + change_to );
  });

  new Swiper('.settingSwiper', {
    slidesPerView: 4,
    spaceBetween: 30,
    centeredSlides: true,
  });
}


// add_new_tile_element

function changePageToNormal() {
  $("body").attr("is_edit_active",false);
  swiper.allowTouchMove = true;
  $(".add_new_tile_element").show().fadeOut(2000);
  $(".exit-edit-mode-button").show().fadeOut(2000);
  $(".bcg-edit").fadeOut(2000);
  setTimeout(() => {
    $("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>" + _("Edit this slide") + "</a>");
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
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

  let SortablePages = document.getElementsByClassName("c_sortable_page_grid");
  
  
  // TODO: smazat
  editMode = true;
  
  swiper.allowTouchMove = false;
  
  $(".add_new_tile_element").hide().fadeIn(2000);
  $(".exit-edit-mode-button").hide().fadeIn(2000);
  $(".bcg-edit").fadeIn(2000);
  
  // Přidělí každému "+" tlačítko Hammer
  $(".add_new_tile_element").each(function() {
    let hammer = new Hammer(this);

    hammer.on("tap", function() {
      addNewTile();
    });
  });
  
  // Vytvoří sortable položky 
  for (let i = 0; i < SortablePages.length; i++) bindSortable(i,SortablePages[i])

  setTimeout(() => {
    $("#edit-page").replaceWith("<a class='dropdown-item' id='edit-page'>" + _("Exit edit mode") + "</a>");
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
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
function destroySortable() {
  for (let i = 0; i < SortableTiles.length; i++) {
    SortableTiles[i].destroy();
  }
}

// Vytvoří Sortable Itemy
function bindSortable(index,item) {
  let temp_element;
  SortableTiles[index] = Sortable.create(item, {
    animation: 150,
    swapThreshold: 1,
    ghostClass: "tile-sortable-move",

    onUpdate: function (evt) {
      socketio.emit("tile_index", {"slide_index": swiper.realIndex, "old_index": evt.oldIndex, "new_index": evt.newIndex});
      // console.log("Slide: " + swiper.realIndex);
      // console.log("Old index: " + evt.oldIndex);
      // console.log("New index: " + evt.newIndex);
    },
    // Element dragging started
	  onStart: function () {
      temp_element = $(".swiper-slide-active").find(".add_new_tile_element").clone();
      $(".swiper-slide-active").find(".add_new_tile_element").remove();
    },  
    onEnd: function () {
      let new_add_modal = $(".swiper-slide-active .c_sortable_page_grid");
      new_add_modal.append(temp_element);

      $(temp_element).each(function(){
        let hammer = new Hammer(this);
        hammer.on("tap", function() {
          addNewTile();
        });
      })

      // $(test_element).appendTo(".c_sortable_page_grid");
    },  
  });
}

// -webkit-user-select: none; -webkit-user-drag: none;
// margin-left: 50px;/* top: -81px; */display: inline-block; box-shadow: none; background-color: transparent; transition: none; -webkit-user-select: none; -webkit-user-drag: none;