/*
*
*   Globální eventy, pro needitovací část
*
*/
$(document).ready(function(){
  SortableTiles = [];

  // Bootstrap dropdown
  $(".dropdown").on("show.bs.dropdown", function(){
    showDropdown(this);
  });

  $(".dropdown").on("hide.bs.dropdown", function(e){
    hideDropdown(this, e);
  });

  $(document.body).on("click", ".edit-page", function() {
    let current_edit_status = store($(document.body), "is-edit-active");
    //DEBUG.logDebug("Current edit status: " + current_edit_status);
    if (current_edit_status === false) changePageToEdit();
    if (current_edit_status === true) changePageToNormal();
  });

  // Button exit edit mode
  $(document.body).on("click", ".exit-edit-mode-button", function() {
    changePageToNormal();
  });

  $(document.body).on("click", ".settings", function() {
    // Request modal - Normal / Edit
    console.log("Requested settings");
    socketio.emit("get_settings_modal", {"tab_id": sessionStorage.tabID});

  });

  $(document.body).on("click", ".client-list", function() {
    // Request modal - Normal / Edit
    console.log("Requested client list");
    socketio.emit("get_client_list_modal", {"tab_id": sessionStorage.tabID});
  });

  $(document.body).on("click", ".user-list", function() {
    console.log("Requested user list");
    socketio.emit("get_user_list_modal", {"tab_id": sessionStorage.tabID});
  });

  $(document.body).on("click", ".doorbird", function() {
    console.log("Requested Doorbird modal");
    socketio.emit("get_doorbird_modal", {"tab_id": sessionStorage.tabID});
  });

  $(document.body).on("click", ".android-apk", function() {
    // Request Android APK download modal
    console.log("Requested Android modal");
    socketio.emit("get_android_modal", {"tab_id": sessionStorage.tabID});
  });

  $(document.body).on("click", ".android-settings", function() {
    // Request Android APK download modal
    console.log("Requested Android settings");
    socketio.emit("show_android_settings");
  });

  $(document.body).on("click", ".logout", function() {
    setTimeout(function(){window.location.href = "/logout";},250);
  });

  $(document.body).on("click", ".reload-all", function() {
    socketio.emit("reload_all");
  });
});

function showDropdown(myThis) {
  $(myThis).find(".dropdown-menu").slideDown();
}

function hideDropdown(myThis, e) {
  e.preventDefault();
    $(myThis).find(".dropdown-menu").first().stop(true, true).slideUp(400, function(){
      $(".dropdown").removeClass("show");
      $(".dropdown-menu").removeClass("show");
      $(".dropdown").find(".dropdown-toggle").attr("aria-expanded", false);
    });
}

function modalClose() {
  $(".modal-here").empty();
  store($(".modal-here"), "type", false)
  $(".clockpicker-popover").hide();
  socketio.emit("modal_close", {"tab_id": sessionStorage.tabID});
}

function displayModal(modal, type, tile_id) {
  store($(".modal-here"), "type", type)
  $("#my-modal").modal("hide");
  $(".btn-close").click().trigger("hide.bs.modal");
    // navigator[vibrate](50);
  $(".modal-here").empty().append(modal);
  $("#my-modal").modal({ keyboard: true }).on("hide.bs.modal", function (e) {
    modalClose();
  });
  let tileID = (typeof tile_id !== "undefined") ? tile_id : null;
  store($(".modal-here"), "tile-id", tileID);

  wait = false;
}

// add_new_tile_element

function changePageToNormal() {

  socketio.emit("edit_change", {"state": false, "tab_id": sessionStorage.tabID});
  store($(document.body), "is-edit-active", false);
  // updateSearchBar();
  swiper.allowTouchMove = true;
  $(".add_new_tile_element").css("transition", "background 0.5s").show().fadeOut(2000, function (){
    $(this).removeAttr("style").hide();
  });
  $(".exit-edit-mode-button").show().fadeOut(2000);
  $(".bcg-edit").fadeOut(2000);
  setTimeout(() => {
    $(".edit-page").text(_("Edit mode"));
    $(".dropdown-wrapper").filter(".disappear-on-normal").each(function() {
      $( this ).css("display", "none");
    });
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
      $( this ).css("display", "block");
    });
  }, 400);
  // TODO: smazat

  destroySortable();
  
  $(".swipe-header").each(function() {
    $( this ).prop("disabled",true)
    $(this).addClass("unselectable");
    // $( this ).css({"border-bottom-width":"0px","border-bottom-style":"none","width":"fit-content"});
  });
}

function changePageToEdit(instantly=false) {
  socketio.emit("edit_change", {"state": true, "tab_id": sessionStorage.tabID});
  store($(document.body), "is-edit-active", true);
  // updateSearchBar();

  let SortablePages = document.getElementsByClassName("c_sortable_page_grid");
  
  swiper.allowTouchMove = false;
  if (!instantly) {
    $(".add_new_tile_element").css("transition", "background 0.5s").hide().fadeIn(2000, function (){
      $(this).removeAttr("style");
    });
    $(".exit-edit-mode-button").hide().fadeIn(2000);
    $(".bcg-edit").fadeIn(2000);
  }

  // Přidělí každému "+" tlačítko Hammer
  $(".add_new_tile_element").each(function() {
    initializeHammerTile(this);
  });
  
  // Vytvoří sortable položky 
  for (let i = 0; i < SortablePages.length; i++) bindSortable(i,SortablePages[i])

  setTimeout(() => {
    $(".edit-page").text(_("Exit edit mode"));
    $(".dropdown-wrapper").filter(".disappear-on-normal").each(function() {
      $( this ).css("display", "block");
    });
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
      $( this ).css("display", "none");
    });
  }, 400);

  $(".swipe-header").each(function() {
    $( this ).prop("disabled",false)
    $(this).removeClass("unselectable");
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
    filter: ".add_new_tile_element",

    onUpdate: function (event) {
      let oldIndex = event.oldDraggableIndex;
      let newIndex = event.newDraggableIndex;

      socketio.emit("tile_index", {"slide_index": swiper.realIndex, "old_index": oldIndex, "new_index": newIndex});
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
        initializeHammerTile(this);
      });
    },
  });
}