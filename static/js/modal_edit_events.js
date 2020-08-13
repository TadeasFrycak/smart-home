/*
*
*   Modal_edit_events.js
*   - definuje eventy při otevřeném modalu v editovacím módu
*
*/

$(document).ready(function(){
  // TODO start at run edit mode

  // Přidání nového modulu v modalu
  $("body").on("click", ".modal-edit-add-item", function() {
    let tile_id = $(".modal-here").attr("id_of_caller");
    let item_name = $.trim($(this).text());

    DEBUG.logDebug("Add new item, Tile ID: " + tile_id + ", Item name: " + item_name)

    socketio.emit("add_modal_item", {
      "type": item_name,
      "tile_id": tile_id
    });
  });

  // Smazání Tilu
  $(document.body).on("click", "#delete-tile", function() {
    let id_of_caller = $(".modal-here").attr("id_of_caller");

    $('#myModal').modal('hide');
    socketio.emit("tile_delete", {"tile_id": id_of_caller});
  });

  // Button collapse all in edit modal
  $(document.body).on("click", "#collapse-items", function() {
    $(".modal-edit-item-dropdown").slideUp();
  });

  // Button unpack all in edit modal
  $(document.body).on("click", "#unpack-items", function() {
    $(".modal-edit-item-dropdown").slideDown();
  });

  // Button scroll up in edit modal
  $(document.body).on("click", "#scroll-up", function() {
    $("#myModal").animate({scrollTop: 0}, "slow");
  });

  // Collapse or unpack one of SortableJS item in modal
  $("body").on("click", ".modal-edit-item", function() {
    if ($(".modal-edit-item-dropdown:hover").length === 0) {
      let status_display = $(this).find(".modal-edit-item-dropdown").css("display");
      if (status_display === "block") $(this).find(".modal-edit-item-dropdown").slideUp();
      if (status_display === "none") $(this).find(".modal-edit-item-dropdown").slideDown();
    }
  });
});

// ( < modal_init.js )
function modalEditItemDelete(object)
{
  let id_of_caller = $(".modal-here").attr("id_of_caller");
  let textbox_wrapper = $(object);
  let wrapper_index = 0

  $(".modal-edit-item").each(function(){
    if ($(this).has(textbox_wrapper).length === 1) return false;
      wrapper_index += 1;
  })
  
  socketio.emit("modal_item_delete", {"tile_id": id_of_caller, "index" : wrapper_index});
}

// Validates a textbox with a minimum number of letters; returns true if OK, false if not
function validateTextBoxWithMinLetters(object, minimumLetters)
{
  let textbox_value = $(object).val();
  if (textbox_value.length <= minimumLetters) { $(object).addClass("is-invalid"); return false;}
  else { $(object).removeClass("is-invalid"); return true;}
}

function validateTextBoxWithRegex(object) {
  let VAL = $(object).val();
  let id_validation_regex = new RegExp("^[a-zA-Z0-9-_]+$");

  if (id_validation_regex.test(VAL)) {
    $(object).removeClass("is-invalid");
    return true;
  }
  $(object).addClass("is-invalid");
  return false;
}

// ( < modal_init.js )
function modalEditItemTextChanged(object) {
  let nameOfThisItem = $(object).parent().parent().find("label").text();
  let feedback = true;

  
  let id_of_caller = $(".modal-here").attr("id_of_caller");
  // let textbox_old_val = $(object).attr("placeholder");
  let textbox_new_val = $(object).val();
  
  if (nameOfThisItem.toLowerCase() === "id") {
    // ( > modal_edit_events.js )
    if (validateTextBoxWithMinLetters(object,5) === false || validateTextBoxWithRegex(object) === false) feedback = false;
    if (feedback) $(object).parent().parent().parent().find(".modal-item-mqtt-path").val("home/" + id_of_caller + "/" + textbox_new_val);
  }


  let textbox_wrapper = $(object);
  let wrapper_index = 0
  console.log(textbox_wrapper);

  // TODO: ?
  $(".modal-edit-item").each(function(){
    if ($(this).has(textbox_wrapper).length === 1) return false;
    wrapper_index += 1;
  });

  if (feedback === true) {
    $(object).attr("placeholder",textbox_new_val);

    socketio.emit("modal_item_dynamic_value", {
      "value_name": nameOfThisItem,
      "tile_id": id_of_caller,
      "new_value": textbox_new_val,
      "index" : wrapper_index
    });
  }
}

// ( < modal_init.js )
function modalEditTileTextChanged(object)
{
  let nameOfThisItem = $(object).parent().parent().find("label").text();

  let id_of_caller = $(".modal-here").attr("id_of_caller");
  // let textbox_old_val = $(object).attr("placeholder");
  let textbox_new_val = $(object).val();

  socketio.emit("tile_dynamic_value", {"value_name": nameOfThisItem, "tile_id": id_of_caller, "new_value": textbox_new_val});  

}

// ( < modal_init.js )
function tileTypeChanged(id_of_caller,type_name) {
  DEBUG.logDebug("Change Tile Type to: " + type_name + " (ID: "+id_of_caller+") ");
  socketio.emit("tile_type", {"tile_id": id_of_caller, "new_type": type_name}); 
}

// ( < modal_init.js )
function modalEditPreviewImageTap(elem) {
  $(".modal-edit-icon").each(function() {
    $(this).css({"border": "2px solid transparent"});
  });
  if ($("body").hasClass("dark")) {
    $(elem.target).css({"border": "2px solid rgb(232, 93, 71)"});
  }
  else {
    $(elem.target).css({"border": "2px solid rgb(23, 162, 184)"});
  }

  let name = $(elem.target).attr("data-name");
  let tile_id = $(".modal-here").attr("id_of_caller");
  
  socketio.emit("tile_icon", {"tile_id": tile_id, "new_icon": name});
}

// ( < modal_init.js )
function modalEditTileTitleChanged() {
  let tile_name = $("#tile_name").val();
  let tile_id = $("#tile-id").val();
  let id_of_caller = $(".modal-here").attr("id_of_caller");

  $("#tile-mqtt-path").val("home/" + tile_id);

  socketio.emit("tile_label", {"tile_id": id_of_caller, "new_label": tile_name});
}

// ( < modal_init.js )
function modalEditTileIDchanged(object) {
  // ( > modal_edit_events.js )
  let feedback = validateTextBoxWithMinLetters(object, 5)
  let id_of_caller = $(".modal-here").attr("id_of_caller");
  let tile_id = $("#tile-id").val();

  if (feedback === true)
  {
    // DEBUG.logDebug("Find item with: " + id_of_caller);
    // DEBUG.logDebug("New ID: " + tile_id);
    socketio.emit("tile_id", {"tile_id": id_of_caller, "new_id": tile_id});
  }

}