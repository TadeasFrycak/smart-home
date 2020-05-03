/*
*
*   modal_edit_events.js
*   - eventy vyvolané interakcí v modalu v normálním režimu
*
*/

$(document).ready(function() {

  // Modal toggle button event on change
  $("body").on("change", ".modal_toggle", function(e){
    var toggleID = $(this).parent().parent().parent().attr("data-id");
    var toggleState = "";
    var tileID = $(".modal-here").attr("id_of_caller");

    e.stopPropagation();
    e.stopImmediatePropagation();

    // Is checked
    if ($(this).prop("checked") === true){
      toggleState = "1";
    }

    // Is unchecked
    else if ($(this).prop("checked") === false){
      toggleState = "0";
    }
    if (toggleID == "dark-mode") {
      $("body").toggleClass("dark");
      $("body").toggleClass("light");
      }

    $.post("/toggle", {
        "id": toggleID,
        "value": toggleState,
        "tile_id": tileID
      }, function(result){});
  });

  
});
