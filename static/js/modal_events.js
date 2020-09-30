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
      toggleState = 1;
    }

    // Is unchecked
    else if ($(this).prop("checked") === false){
      toggleState = 0;
    }
    console.log(toggleState);
    socketio.emit("modal_toggle", {"id": toggleID, "value": toggleState, "tile_id": tileID});
  });
});