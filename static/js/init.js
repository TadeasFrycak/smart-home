$(document).ready(function(){
  /*
  *
  *   Inicializování předmětů (při i po načtení stránky)
  *
  */

  // terminal.log("+----------------------------------+");
  // terminal.log("|                                  |");
  // terminal.log("|          Smart home 11.4         |");
  // terminal.log("|     Author: Szkandera, Fryčák    |");
  // terminal.log("|                                  |");
  // terminal.log("|          ©  2019 - 2020          |");
  // terminal.log("|                                  |");
  // terminal.log("+----------------------------------+");

  console.log("   _____                      _     _                          \n" +
      "  / ____|                    | |   | |                         \n" +
      " | (___  _ __ ___   __ _ _ __| |_  | |__   ___  _ __ ___   ___ \n" +
      "  \\___ \\| '_ ` _ \\ / _` | '__| __| | '_ \\ / _ \\| '_ ` _ \\ / _ \\\n" +
      "  ____) | | | | | | (_| | |  | |_  | | | | (_) | | | | | |  __/\n" +
      " |_____/|_| |_| |_|\\__,_|_|   \\__| |_| |_|\\___/|_| |_| |_|\\___|\n" +
      "                                                               \n")

  $(".swiper-pagination").dblclick(function(){
    toggleFullscreen();
});
  function toggleFullscreen(elem) {
  elem = elem || document.documentElement;

  if (!document.fullscreenElement && !document.mozFullScreenElement &&
    !document.webkitFullscreenElement && !document.msFullscreenElement) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
}
  // Vytvoření DEBUG objektu
  DEBUG = new debug_console();

  /*
  *
  *   Statické eventy po načtení stránky   
  *
  */

  // Hide elements visible only in
  let isEditActive = $("body").attr("data-is-edit-active");
  if (isEditActive === "false") {
    $(".dropdown-wrapper").filter(".disappear-on-normal").each(function() {
      $( this ).css("display", "none");
    });
  }

  else {
    changePageToEdit(true);
  }

  let tileID = $(".swipe-body").attr("data-modal-id");
  let tileType = $(".swipe-body").attr("data-modal-type");
  if (tileType === "normal" && tileID) {
    socketio.emit("get_modal", {"tile_id": tileID, "tab_id": sessionStorage.tabID})
  }
  else if (tileType === "edit" && tileID) {
    socketio.emit("get_edit_modal", {"tile_id": tileID, "tab_id": sessionStorage.tabID})
  }
  else if (tileType === "client_list" && tileID) {
    socketio.emit("get_client_list_modal", {"tab_id": sessionStorage.tabID})
  }
  else if (tileType === "user_list" && tileID) {
    socketio.emit("get_user_list_modal", {"tab_id": sessionStorage.tabID})
  }
  else if (tileType === "android" && tileID) {
    socketio.emit("get_android_modal", {"tab_id": sessionStorage.tabID})
  }
  else if (tileType === "settings" && tileID) {
    socketio.emit("get_settings_modal", {"tab_id": sessionStorage.tabID})
  }

  if (location.hash !== "" || location.search !== "") {
    console.log("Cleaning URL...");
    window.history.pushState("", "", "/");
  }
  resize();

  // Name of page changed
  $(".swipe-header").on("input", function(){
    let nameOfPageChanged = $(this).val();
    socketio.emit("slide_name", {"index": swiper.realIndex, "new_name": nameOfPageChanged});
  });
});

// $(window).resize(resize).trigger("resize");
let doit
window.onresize = function(){
  clearTimeout(doit);
  doit = setTimeout(resize, 10);
};
function resize() {
  const tileWidth = 112
  let width = $(".swipe-content").width()
  let howMany = (width)/tileWidth;
  howMany = Math.floor(howMany); // Round down
  let tilesWidth = Math.ceil(howMany*tileWidth+1); // Round up
  // terminal.log(tilesWidth);
  $(".c_sortable_page_grid").css("width", tilesWidth);
}

class debug_console {
  log(data) {
    console.log(data);
  }

  logLabeled(string,data) {
    console.log(`${string} : ${data}`);
  }

  logWarning(data) {
    console.log(`%cWARNING : %c${data} `, 'color: red','color: black');
  }

  logDebug(data) {
    console.log(`%cDEBUG : %c${data} `, 'color: grey','color: black');
  }
}
