$(document).ready(function(){
  /*
  *
  *   Inicializování předmětů (při i po načtení stránky)
  *
  */

  console.log("+----------------------------------+");
  console.log("|      " + _("Smart home") + " 11.3       |");
  console.log("|    " + _("authors:") + " Fryčák, Szkandera     |");
  console.log("|                                  |");
  console.log("|          ©  2019 - 2020          |");
  console.log("+----------------------------------+");

  // Odejít ze stránky není tak jednoduché
  //window.onbeforeunload = function() {
  //  return true;
  //};

  // Vytvoření DEBUG objektu
  DEBUG = new debug_console();

  editMode = false;

  /*
  *
  *   Statické eventy po načtení stránky   
  *
  */

  // Zavádění atributu pro detekci módu (normal - false / edit - true)
  //$("body").attr("is_edit_active",false);

  // Hide elements visible only in 
  let isEditActive = $("body").attr("is_edit_active");
  if (isEditActive === "false") {
    $(".dropdown-wrapper").filter(".disappear-on-edit").each(function() {
      $( this ).css("display","none");
    });
  }
  else {
    changePageToEdit()
  }

  // Scale page
  /*var window_width = window.innerWidth;
  var window_height = window.innerHeight;

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
