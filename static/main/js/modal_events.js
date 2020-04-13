$(document).ready(function() {
  // ----------------------------------------------
  // Modal events
  // ----------------------------------------------

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

    $.post("/toggle", {
        "id": toggleID,
        "value": toggleState,
        "tile_id": tileID
      }, function(result){});
  });
});