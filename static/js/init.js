// Instant changes
 let modalData = isModalOpen(null, null, true);
if (modalData) {
  wait = true;
}

// Hide elements visible only in
let isEditActive = store($(document.body), "is-edit-active");
if (isEditActive === true) {

  $(".add_new_tile_element").show();
  $(".exit-edit-mode-button").show();
  $(".bcg-edit").show();
}
resize();

$(document).ready(function(){
  /*
  *
  *   Inicializování předmětů (při i po načtení stránky)
  *
  */

  console.log(
            "  _____ _    _         \n" +
            " / ____| |  | |  Smart \n" +
            "| (___ | |__| |  Home  \n" +
            " \\___ \\|  __  |      \n" +
            " ____) | |  | |        \n" +
            "|_____/|_|  |_|        \n\n")

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
  let isEditActive = store($(document.body), "is-edit-active");
  if (isEditActive === false) {
    $(".dropdown-wrapper").filter(".disappear-on-normal").each(function() {
      $( this ).css("display", "none");
    });
  }

  else {
    changePageToEdit(true);
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
