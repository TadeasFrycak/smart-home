$(document).ready(function(){
  // ----------------------------------------------
  // Global initialisation
  // ----------------------------------------------

  console.log("+----------------------------------+");
  console.log("|         Chytrý Fryčák 11.0       |");
  console.log("|     Autor: Fryčák, Szkandera     |");
  console.log("|                                  |");
  console.log("|          ©  2019 - 2020          |");
  console.log("+----------------------------------+");

  // console.log('%c Oh my heavens! ', 'background: #222; color: #bada55');
  init_page();

  // var lastWidth;
  // var lastHeight;

  function zoom() {
    // Scale page
    var width = $(".zoomable").width();
    var howMany = Math.floor(width/112);
    var tilesWidth = howMany*112;
    var zoom = width/tilesWidth;

    //$(".zoomable").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom, "-moz-transform": "scale(" + zoom + "," + zoom + ")", "-moz-transform-origin": "left center"});
    $(".zoomable").css({"zoom": zoom, "-ms-zoom": zoom, "-webkit-zoom": zoom});
    //$(".zoomable").css({"zoom":zoom});
  }

  // window.onresize = function() {
  //  width = $(window).width();
  //  height = $(window).height();
  //  if (((width - 100) > lastWidth || (width + 100) < lastWidth) && ((height - 100) > lastHeight || (height + 100) < lastHeight)) {
  //    setTimeout(() => {zoom();}, 1000);
  //  }

  //  lastWidth = $(window).width();
  //  lastHeight = $(window).height();
  //}

  zoom();
  //lastWidth = $(window).width();
  //lastHeight = $(window).height();
});

function init_page()
{
  // Define some global variables
  deviceNumber = Math.round(Math.random() * 1000);
  editMode = false;
  sliders = [];

  // Tile statuses
  $(".tileStatus").each(function() {
    if ($(this).text() === "ON"){
      $(this).parent().parent().toggleClass("tileActive");
      $(this).parent().parent().find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
    }
  });

  // Tile toggles
  $(".tileToggle").each(function(){
    tileToggleTap(this)
  });
}

function tileToggleTap(this_)
{
  var $this = $(this_);
  var hammer = new Hammer(this_);

  hammer.on("tap", function() {
    if (editMode == false)
    {
      $this.parent().toggleClass("tileActive");
      var tileID = $this.parent().attr("data-id");
      var tileState = $this.parent().find(".tileStatus").text();

      if (tileState === "ON") {
        tileState = "OFF";
        $this.parent().find(".tileStatus").text("OFF");
        $this.parent().find(".toggle-dot").css("background-color", "rgba(255, 0, 0, 0.28)");
      }

      else if (tileState === "OFF") {
        tileState = "ON";
        $this.parent().find(".tileStatus").text("ON");
        $this.parent().find(".toggle-dot").css("background-color", "rgba(0, 196, 42, 0.28)");
      }

      $.post("/tile", {
          "id": tileID,
          "value": tileState
        }, function(result) {}
      );
    }

  });
}
