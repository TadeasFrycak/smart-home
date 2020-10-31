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

  $("body").on("click", ".edit-page", function() {
    let current_edit_status = $("body").attr("data-is-edit-active");
    //DEBUG.logDebug("Current edit status: " + current_edit_status);
    if (current_edit_status === "false") changePageToEdit();
    if (current_edit_status === "true") changePageToNormal();
  });

  // Button exit edit mode
  $("body").on("click", ".exit-edit-mode-button", function() {
    changePageToNormal();
  });

  $("body").on("click", ".settings", function() {
    // Request modal - Normal / Edit
    console.log("Requested settings");
    socketio.emit("get_settings_modal", {"tab_id": sessionStorage.tabID});

  });

  $("body").on("click", ".client-list", function() {
    // Request modal - Normal / Edit
    console.log("Requested client list");
    socketio.emit("get_client_list_modal", {"tab_id": sessionStorage.tabID});
  });

  $("body").on("click", ".user-list", function() {
    console.log("Requested user list");
    socketio.emit("get_user_list_modal", {"tab_id": sessionStorage.tabID});
  });

  $("body").on("click", ".android-apk", function() {
    // Request Android APK download modal
    console.log("Requested Android modal");
    socketio.emit("get_android_modal", {"tab_id": sessionStorage.tabID});
  });

  $("body").on("click", ".android-settings", function() {
    // Request Android APK download modal
    console.log("Requested Android settings");
    socketio.emit("show_android_settings");
  });

  $("body").on("click", ".shutdown", function() {
    $.post("/shutdown", {});
  });

  $("body").on("click", ".logout", function() {
    setTimeout(function(){window.location.href = "/logout";},250);
  });

  $("body").on("click", ".reload-all", function() {
    socketio.emit("reload_all");
  });

  $("body").on("click", ".restart", function() {
    $.post("/restart", {});
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
      $(".dropdown").find(".dropdown-toggle").attr("aria-expanded","false");
    });
}

function modalClose() {
  $(".modal-here").empty();
  $(".clockpicker-popover").hide();
  socketio.emit("modal_close", {"tab_id": sessionStorage.tabID});
}

function displaySettingsModal(result){
  // var json = JSON.parse(result);

  $(".modal-here").empty().append(result.modal);
  $("#myModal").modal({ keyboard: true });
  $("#myModal").on("hide.bs.modal", function (e) {
    modalClose();
  });

  $( ".modal-settings-page-appearance" ).click(function() {
    let change_to = $(this).attr("data-type");
    socketio.emit("user_mode", {"mode": change_to});
    console.log( "Change appearance to " + change_to );
    modalSettingsAppearanceImageTap(this);
  });

  $('.fotorama')
        // Listen to the events
      // TODO tohle není ten správný event, reaguje po načtení obrázku, ne po zvolení
        .on('fotorama:showend ',  // Stage image of some frame is loaded
            function (e, fotorama, extra) {
              // terminal.log('## ' + e.type);
              // terminal.log('active frame', fotorama.activeFrame);
              // terminal.log('additional data', extra);
              let background = fotorama.activeFrame.img.split("/");
              socketio.emit("user_background", {"background": background[background.length-1]})
            }
        )
        // Initialize fotorama manually
        .fotorama({
    allowfullscreen: true,
    nav: "thumbs",
    keyboard: {"home": true, "end": true},
  });

  // new Swiper('.settingSwiper', {
  //   slidesPerView: 4,
  //   spaceBetween: 30,
  //   centeredSlides: true,
  // });
}

// add_new_tile_element

function changePageToNormal() {

  socketio.emit("edit_change", {"state": false, "tab_id": sessionStorage.tabID});
  $("body").attr("data-is-edit-active", false);
  // updateSearchBar();
  swiper.allowTouchMove = true;
  $(".add_new_tile_element").show().fadeOut(2000);
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
    $( this ).prop("readonly",true)
    // $( this ).css({"border-bottom-width":"0px","border-bottom-style":"none","width":"fit-content"});
  });
}

function changePageToEdit(instantly=false) {
  socketio.emit("edit_change", {"state": true, "tab_id": sessionStorage.tabID});
  $("body").attr("data-is-edit-active", true);
  // updateSearchBar();

  let SortablePages = document.getElementsByClassName("c_sortable_page_grid");
  
  swiper.allowTouchMove = false;
  if (instantly) {
    $(".add_new_tile_element").show();
    $(".exit-edit-mode-button").show();
    $(".bcg-edit").show();
  }
  else {
    $(".add_new_tile_element").hide().fadeIn(2000);
    $(".exit-edit-mode-button").hide().fadeIn(2000);
    $(".bcg-edit").fadeIn(2000);
  }

  
  // Přidělí každému "+" tlačítko Hammer
  $(".add_new_tile_element").each(function() {
    let hammer = new Hammer(this);

    // hammer.on("tap", function() {
    //   addNewTile();
    // });
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
      // terminal.log("Slide: " + swiper.realIndex);
      // terminal.log("Old index: " + evt.oldIndex);
      // terminal.log("New index: " + evt.newIndex);
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

      // $(temp_element).each(function(){
      //   let hammer = new Hammer(this);
      //   hammer.on("tap", function() {
      //     addNewTile();
      //   });
      // })

      // $(test_element).appendTo(".c_sortable_page_grid");
    },  
  });
}

// -webkit-user-select: none; -webkit-user-drag: none;
// margin-left: 50px;/* top: -81px; */display: inline-block; box-shadow: none; background-color: transparent; transition: none; -webkit-user-select: none; -webkit-user-drag: none;