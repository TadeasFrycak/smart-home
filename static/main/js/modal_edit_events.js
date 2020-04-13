$(document).ready(function(){
  // ----------------------------------------------
  // Modal edit mode events
  // ----------------------------------------------

  // TODO start at run edit mode

  // SortableJS item in modal
  $("body").on("click", ".modal_add_new_item", function(e) {
    var tile_id = $(".modal-here").attr("id_of_caller");
    $.post("/add_modal_edit_item", {
        "type": $(this).text(),
        "tile_id": tile_id
      }, function(result){
        var json = JSON.parse(result);
        $(".modal_items_edit_sortable").prepend($(json.item));
        var item = $(".modal_items_edit_sortable").find(".modal_items_edit_sortable_item")[0];
        
        $(item).attr("id","modal_items_edit_sortable_last");
        $("#modal_items_edit_sortable_last").hide().slideDown();
        $("#modal_items_edit_sortable_last").removeAttr("id");
    });
  });

  // Delete tile button in modal
  $(document.body).on("click", "#delete-tile", function(e) {
    var id_of_caller = $(".modal-here").attr("id_of_caller");

    $('#myModal').modal('hide');
    $.post( "/tile_delete", {
        "id": id_of_caller,
    });
  });

  // Button collapse all in edit modal
  $(document.body).on("click", "#collapse-items", function(e) {
    $(".modal_items_edit_sortable_item_dropdown").slideUp();
  });

  // Button unpack all in edit modal
  $(document.body).on("click", "#unpack-items", function(e) {
    $(".modal_items_edit_sortable_item_dropdown").slideDown();
  });

  // Button scroll up in edit modal
  $(document.body).on("click", "#scroll-up", function(e) {
    $("#myModal").animate({scrollTop: 0}, "slow");
  });

  // Collapse or unpack one of SortableJS item in modal
  $("body").on("click", ".modal_items_edit_sortable_item", function(e) {
    if ($(".modal_items_edit_sortable_item_dropdown:hover").length == 0) {
      var status_display = $(this).find(".modal_items_edit_sortable_item_dropdown").css("display");
      if (status_display == "block") $(this).find(".modal_items_edit_sortable_item_dropdown").slideUp();
      if (status_display == "none") $(this).find(".modal_items_edit_sortable_item_dropdown").slideDown();
    }
  });
});