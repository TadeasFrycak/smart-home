$(document).ready(function(){
  /*
  *
  *   Inicializování předmětů (při i po načtení stránky)
  *
  */

  console.log("+----------------------------------+");
  console.log("|   Chytrá domácnost (Beta)11.1    |");
  console.log("|    Autoři: Fryčák, Szkandera     |");
  console.log("|                                  |");
  console.log("|          ©  2019 - 2020          |");
  console.log("+----------------------------------+");

  // Forbid mouse right click
  // document.addEventListener("contextmenu", event => event.preventDefault());

  // Odejít ze stránky není tak jednoduché
  //window.onbeforeunload = function() {
  //  return true;
  //};

  // Vytvoření DEBUG objektu
  DEBUG = new debug_console();

  deviceNumber = Math.round(Math.random() * 1000);
  editMode = false;

  // TODO: globální proměnná pro slidery
  sliders = [];

  /*
  *
  *   Statické eventy po načtení stránky   
  *
  */

 

  // Zavádění atributu pro detekci módu (normal - false / edit - true)
  //$("body").attr("is_edit_active",false);

  // Hide elements visible only in 
  var isEditActive = $("body").attr("is_edit_active");
  if (isEditActive == "false")
  {
    $(".dropdown-wrapper[dissapear-on-edit]").each(function() {
      $( this ).css("display","none");
    });
  }
  else {
    changePageToEdit()
  }

  // Scale page
  var window_width = window.innerWidth;
  var window_height = window.innerHeight;

  // If device is mobile
  /*if (window_height >= window_width) {
    var width = $(".zoomable").width();
    var howMany = width/116;
    howMany = Math.round(howMany-0.1);
    var tilesWidth = howMany*116;
    console.log(tilesWidth);
    var zoom = width/tilesWidth;
    //$(".zoomable").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom, "-moz-transform": "scale(" + zoom + "," + zoom + ")", "-moz-transform-origin": "left center"});
    $(".zoomable").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom});
  }*/

  $(".tileToggle").each(function(){
    initializeTileWithTap(this);
  });

  // Přidělí každému Tilu, který má povolený Modal, Hammer stisknutí
  $(".tileModal").each(function(){
    var $this = $(this);
    var hammer = new Hammer(this);
    initTilePress(hammer, $this,0);
  });

  // Name of page changed
  $(".swipe-header-textbox").on("input",function(){
    var nameOfPageChanged = $(this).val();
    $.post("/slide_name", {
      "index": swiper.realIndex,
      "new_name": nameOfPageChanged,
    }, function(){});
  });
});

function initializeTileWithTap(object)
{
  // Při načtení upravit TOGGLE item podle jeho stavu (při jiném než Toggle itemu = undefined)
  //if ($(object).parent().find(".tileStatus").text() === "ON"){
    //$(object).parent().toggleClass("tileActive");
    //$(object).parent().css("opacity", 1);
    // TODO NASTAVENÍ
    // $(object).parent().css({"-moz-transform": "scale(1.03)", "-webkit-transform": "scale(1.03)", "transform": "scale(1.03)"})
    //$(object).parent().find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");

  //}
  //else {
  //  $(object).parent().css("opacity", 0.7);
  //}

  // Připnout Hammer každému itemu
  var $this = $(object);
  var hammer = new Hammer(object);
  hammer.on("tap", function() {
    // ( > events.js )
    tappedOnToggle($this)
  });
}

class debug_console{

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
