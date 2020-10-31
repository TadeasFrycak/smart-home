/*
*
*   modal_edit_events.js
*   - eventy vyvolané interakcí v modalu v normálním režimu
*
*/

$(document).ready(function() {
  // Modal toggle button event on change
  $("body").on("change", ".modal-toggle-input", function(e){
    let toggleID = $(this).parent().parent().attr("data-id");
    let toggleState = "";
    let tileID = $(".modal-here").attr("id_of_caller");

    console.log(toggleID);
    console.log(tileID);
    e.stopPropagation();
    e.stopImmediatePropagation();

    // Is checked
    if ($(this).prop("checked") === true){
      toggleState = true;
    }

    // Is unchecked
    else if ($(this).prop("checked") === false){
      toggleState = false;
    }

    let attr = $(this).parent().parent().parent().attr("data-static");
    if (typeof attr !== typeof undefined && attr !== false){
      socketio.emit("tile_value", {"value": {[toggleID]: toggleState}, "tile_id": tileID});
    }
    else{
      socketio.emit("modal_toggle", {"id": toggleID, "value": toggleState, "tile_id": tileID});
    }

  });
});