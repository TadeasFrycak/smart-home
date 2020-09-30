$(document).ready(function(){
  /*
  *
  *   Inicializování předmětů (při i po načtení stránky)
  *
  */

  // console.log("+----------------------------------+");
  // console.log("|                                  |");
  // console.log("|          Smart home 11.4         |");
  // console.log("|     Author: Szkandera, Fryčák    |");
  // console.log("|                                  |");
  // console.log("|          ©  2019 - 2020          |");
  // console.log("|                                  |");
  // console.log("+----------------------------------+");

  console.log("   _____                      _     _                          \n" +
      "  / ____|                    | |   | |                         \n" +
      " | (___  _ __ ___   __ _ _ __| |_  | |__   ___  _ __ ___   ___ \n" +
      "  \\___ \\| '_ ` _ \\ / _` | '__| __| | '_ \\ / _ \\| '_ ` _ \\ / _ \\\n" +
      "  ____) | | | | | | (_| | |  | |_  | | | | (_) | | | | | |  __/\n" +
      " |_____/|_| |_| |_|\\__,_|_|   \\__| |_| |_|\\___/|_| |_| |_|\\___|\n" +
      "                                                               \n")
  // console.log("\n" +
  //     "  ___                _     _                  \n" +
  //     " / __|_ __  __ _ _ _| |_  | |_  ___ _ __  ___ \n" +
  //     " \\__ \\ '  \\/ _` | '_|  _| | ' \\/ _ \\ '  \\/ -_)\n" +
  //     " |___/_|_|_\\__,_|_|  \\__| |_||_\\___/_|_|_\\___|\n" +
  //     "                                              \n")
  // Odejít ze stránky není tak jednoduché
  //window.onbeforeunload = function() {
  //  return true;
  //};


  // Vytvoření DEBUG objektu
  DEBUG = new debug_console();

  /*
  *
  *   Statické eventy po načtení stránky   
  *
  */

  // Zavádění atributu pro detekci módu (normal - false / edit - true)
  //$("body").attr("data-is-edit-active",false);

  window.onbeforeunload = function(event) {
    window.setTimeout(function () {
      beforeRefresh();
      window.location = window.location.href;
    }, 0);
    window.onbeforeunload = null;
  };

  // Hide elements visible only in 
  let isEditActive = $("body").attr("data-is-edit-active");
  if (isEditActive === "false") {
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
      $( this ).css("display","none");
    });
    let tile = $(".swipe-body").attr("data-modal-start");
    if (tile) {
      socketio.emit("get_modal", {"tile_id": tile})
    }
  }

  else {
    changePageToEdit(instantly=true)
    let tile = $(".swipe-body").attr("data-modal-start");
    if (tile) {
      socketio.emit("get_edit_modal", {"tile_id": tile})
    }
  }

  window.history.pushState("", "", "/");
  resize();

  // Scale page
  /*var window_width = window.innerWidth;
  var window_height = window.innerHeight;

  c_sortable_page_grid

  if (window_height >= window_width) {
    var width = $(".c_sortable_page_grid").width();
    var howMany = width/116;
    howMany = Math.round(howMany-0.1);
    var tilesWidth = howMany*116;
    console.log(tilesWidth);
    var zoom = width/tilesWidth;
    //$(".c_sortable_page_grid").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom, "-moz-transform": "scale(" + zoom + "," + zoom + ")", "-moz-transform-origin": "left center"});
    $(".c_sortable_page_grid").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom});
  }*/

  // Name of page changed
  $(".swipe-header-textbox").on("input",function(){
    let nameOfPageChanged = $(this).val();
    socketio.emit("slide_name", {"index": swiper.realIndex, "new_name": nameOfPageChanged});
  });
});

$( window ).resize(function() {
  resize();
});


function resize()
{
  // let MARGIN = 15;
  //
  // let window_width = window.innerWidth * 0.99;
  //
  // console.log(window_width);
  //
  // let box_width = (Math.floor(window_width / 110)-1)*110;
  //
  // $(".c_sortable_page_grid").css("width", box_width + MARGIN);
  // console.log(box_width);

  let width = $(".swipe-content").width()
  let howMany = width/113;
  howMany = Math.floor(howMany);
  let tilesWidth = howMany*113;
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
