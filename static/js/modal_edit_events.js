/*
*
*   Modal_edit_events.js
*   - definuje eventy při otevřeném modalu v editovacím módu
*
*/

$(document).ready(function(){

  // ? ->
  // TODO start at run edit mode

  // Přidání nového modulu v modalu
  $("body").on("click", ".modal_add_new_item", function(e) {

    var tile_id = $(".modal-here").attr("id_of_caller");
    var item_name = $.trim($(this).text());

    DEBUG.logDebug("Add new item, Tile ID: " + tile_id + ", Item name: " + item_name)

    $.post("/add_modal_edit_item", {
      "type": item_name,
      "tile_id": tile_id
    }, 
    function(result){
      var json = JSON.parse(result);
      $(".modal_items_edit_sortable").prepend($(json.item));
      var item = $(".modal_items_edit_sortable").find(".modal_items_edit_sortable_item")[0];
      
      $(item).attr("id","modal_items_edit_sortable_last");
      $("#modal_items_edit_sortable_last").hide().slideDown();
      $("#modal_items_edit_sortable_last").removeAttr("id");

      $(item).find(".modal_edit_item_textbox").on("input",function(e){
        // ( > modal_edit_events.js )
        modalEditItemTextChanged(this);
      });
    });
  });

  // Smazání Tilu
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


// ( < modal_init.js )
function modalEditItemDelete(object)
{
  var id_of_caller = $(".modal-here").attr("id_of_caller");

  var textbox_wrapper = $(object);
  var wrapper_index = 0

  $(".modal_items_edit_sortable_item").each(function(e){
    if ($(this).has(textbox_wrapper).length == 1) return false;
      wrapper_index += 1;
  })
  
  $.post( "/modal_item_delete", {
    "tile_id": id_of_caller,
    "index" : wrapper_index
  });

  $(object).parent().parent().parent().slideUp();
  setTimeout(() => {$(object).parent().parent().parent().remove();}, 600);
}

// Validates a textbox with a minimum number of letters; returns true if OK, false if not
function validateTextBoxWithMinLetters(object, minimumLetters)
{
  var textbox_value = $(object).val();
  if (textbox_value.length <= minimumLetters) { $(object).addClass("is-invalid"); return false;}
  else { $(object).removeClass("is-invalid"); return true;}
}

function validateTextBoxWithregex(object)
{
  var VAL = $(object).val();

  var id_validation_regex = new RegExp("^[a-zA-Z0-9-_]+$");

  if (id_validation_regex.test(VAL)) {
    $(object).removeClass("is-invalid");
    return true;
  }
  $(object).addClass("is-invalid");
  return false;
}

// ( < modal_init.js )
function modalEditItemTextChanged(object)
{
  var nameOfThisItem = $(object).parent().parent().find("label").text();
  var feedback = true;

  
  var id_of_caller = $(".modal-here").attr("id_of_caller");
  var textbox_old_val = $(object).attr("placeholder");
  var textbox_new_val = $(object).val();
  
  if (nameOfThisItem.toLowerCase() == "id")
  {
    // ( > modal_edit_events.js )
    if (validateTextBoxWithMinLetters(object,5) == false || validateTextBoxWithregex(object) == false) feedback = false;

    if (feedback) $(object).parent().parent().parent().find(".modal-item-mqtt-path").val("home/" + id_of_caller + "/" + textbox_new_val);
  }

  DEBUG.logDebug("Old value: " + textbox_old_val);
  DEBUG.logDebug("New value: " + textbox_new_val);

  var textbox_wrapper = $(object);
  var wrapper_index = 0
  console.log(textbox_wrapper);

  // TODO: ?
  $(".modal_items_edit_sortable_item").each(function(){
    if ($(this).has(textbox_wrapper).length == 1)
    {
      return false;
    }
      wrapper_index += 1;
  });

  if (feedback == true)
  {
    $(object).attr("placeholder",textbox_new_val);

    $.post("/modal_item_value_rwr", {
      "value_name": nameOfThisItem,
      "tile_id": id_of_caller,
      "old_value": textbox_old_val,
      "new_value": textbox_new_val,
      "index" : wrapper_index
    });
  }


}

// ( < modal_init.js )
function modalEditTileTextChanged(object)
{
  var nameOfThisItem = $(object).parent().parent().find("label").text();

  var id_of_caller = $(".modal-here").attr("id_of_caller");
  // TODO: unused variable
  var textbox_old_val = $(object).attr("placeholder");
  var textbox_new_val = $(object).val();

  $.post("/tile_dynamic_value_rwr", {
    "value_name": nameOfThisItem,
    "tile_id": id_of_caller,
    "new_value": textbox_new_val,
  });  

}

// ( < modal_init.js )
function tileTypeChanged(id_of_caller,type_name)
{
  DEBUG.logDebug("Change Tile Type to: " + type_name + " (ID: "+id_of_caller+") ");
  $.post( "/tile_type_rwr", {
    "id": id_of_caller,
    "new_type": type_name
  }, 
  function(response){

    var json = JSON.parse(response);
    console.log(json);
    $(".tile-type-wrapper").empty();
    $(".tile-type-wrapper").append(json.tile_values);

    initImages();

  });
}

// ( < modal_init.js )
function modalEditPreviewImageTap(elem)
{
  $(".modal-edit-select-img").each(function() {
    $(this).css({"border": "2px solid transparent"});
  });
  $(elem.target).css({"border": "2px solid rgb(23, 162, 184)"});
  var name = $(elem.target).attr("-data-name");
  var tile_id = $(".modal-here").attr("id_of_caller");
  
  $.post( "/tile_icon_rwr", {
    "id": tile_id,
    "new_icon": name
  }, function(){});
}

// ( < modal_init.js )
function modalEditTileTitleChanged()
{
  var tile_name = $("#tile_name").val();
  var tile_id = $("#tile-id").val();
  var id_of_caller = $(".modal-here").attr("id_of_caller");

  $("#tile-mqtt-path").val("home/" + tile_id);

  $.post( "/tile_name_rwr", {
    "tile_id": id_of_caller,
    "new_name": tile_name
  });
}

// ( < modal_init.js )
function modalEditTileIDchanged(object)
{
  // ( > modal_edit_events.js )
  var feedback = validateTextBoxWithMinLetters(object, 5)

  var id_of_caller = $(".modal-here").attr("id_of_caller");
  var tile_id = $("#tile-id").val();

  if (feedback == true)
  {
    DEBUG.logDebug("Find item with: " + id_of_caller);
    DEBUG.logDebug("New ID: " + tile_id);
    $(".tile[data-id='"+id_of_caller+"']").attr("data-id",tile_id);
    $("#tile-mqtt-path").val("home/" + tile_id);
    $(".modal-here").attr("id_of_caller", tile_id);

    $.post( "/tile_id_rwr", {
      "tile_id": id_of_caller,
      "new_id": tile_id
    });
  }

}