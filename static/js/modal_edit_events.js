/*
*
*   Modal_edit_events.js
*   - definuje eventy při otevřeném modalu v editovacím módu
*
*/

$(document).ready(function(){
  // TODO start at run edit mode

  // Přidání nového modulu v modalu
  $(document.body).on("click", ".modal-edit-add-item", function() {
    let tile_id = store($(".modal-here"), "tile-id");
    let item_name = store($(this), "type");

    DEBUG.logDebug("Add new item, Tile ID: " + tile_id + ", Item name: " + item_name)

    socketio.emit("modal_item_prepend", {
      "type": item_name,
      "tile_id": tile_id
    });
  });

  // Smazání Tilu
  $(document.body).on("click", "#delete-tile", function() {
    let tileID = store($(".modal-here"), "tile-id");

    $('#my-modal').modal('hide');
    socketio.emit("tile_delete", {"tile_id": tileID});
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
    $("#my-modal").animate({scrollTop: 0}, "slow");
  });

  // Collapse or unpack one of SortableJS item in modal
  $(document.body).on("click", ".modal-edit-item", function(e) {
    e.stopPropagation();
    if (!($(e.target).hasClass("no-open"))) {
      if ($(".modal-edit-item-dropdown:hover").length === 0) {
        let status_display = $(this).find(".modal-edit-item-dropdown").css("display");
        if (status_display === "block") $(this).find(".modal-edit-item-dropdown").slideUp();
        if (status_display === "none") $(this).find(".modal-edit-item-dropdown").slideDown();
      }
    }
  });
});

// ( < modal_init.js )
function modalEditItemDelete(object) {
  let tileID = store($(".modal-here"), "tile-id");
  socketio.emit("modal_item_delete", {"tile_id": tileID, "id" : store($(object).closest(".modal-edit-item"), "id")});
}

// Validates a value with a minimum number of letters; returns true if OK, false if not
function validateID(value) {
  let idValidationRegex = new RegExp("^[a-zA-Z0-9-_]+$");
  return idValidationRegex.test(value) && value.length > 5;
}

// ( < modal_init.js )
function modalEditItemTextChanged(object) {
  let itemName = store($(object), "id");
  let tileID = store($(".modal-here"), "tile-id");
  let newValue = store($(object), "value");
  socketio.emit("modal_item_config", {
    "value_name": itemName,
    "tile_id": tileID,
    "id": store($(object).closest(".modal-edit-item"), "id"),
    "new_value": newValue,
  });
}

// ( < modal_init.js )
function modalEditTileTextChanged(object) {
  let nameOfThisItem = $(object).parent().parent().find("label").text();

  let tileID = store($(".modal-here"), "tile-id");
  // let textbox_old_val = $(object).attr("placeholder");
  let textbox_new_val = $(object).val();

  socketio.emit("tile_dynamic_value", {"value_name": nameOfThisItem, "tile_id": tileID, "new_value": textbox_new_val});
}

// ( < modal_init.js )
function tileTypeChanged(tileID,type_name) {
  DEBUG.logDebug("Change Tile Type to: " + type_name + " (ID: "+tileID+") ");
  socketio.emit("tile_type", {"tile_id": tileID, "new_type": type_name});
}

// ( < modal_init.js )
function modalEditPreviewImageTap(elem) {
  $(".modal-edit-icon").each(function() {
    $(this).css({"border": "2px solid transparent"});
    store($(this), 'selected',false);
  });
  if ($(document.body).hasClass("dark")) {
    $(elem.target).css({"border": "2px solid rgb(232, 93, 71)"});
  }
  else {
    store($(elem.target), 'selected',true);
    $(elem.target).css({"border": "2px solid rgb(23, 162, 184)"});
  }

  let name = store($(elem.target), "name");
  let tile_id = store($(".modal-here"), "tile-id");
  
  socketio.emit("tile_icon", {"tile_id": tile_id, "new_icon": name});
}

// ( < modal_init.js )
function modalEditTileTitleChanged() {
  let tile_name = $("#tile_name").val();
  // let tile_id = $("#tile-id").val();
  let tileID = store($(".modal-here"), "tile-id");

  // $("#tile-mqtt-path").val("home/" + tile_id);

  socketio.emit("tile_label", {"tile_id": tileID, "new_label": tile_name});
}

// ( < modal_init.js )
function modalEditTileIDchanged(object) {
  // ( > modal_edit_events.js )
  if (validateID($(object).val()) === true) {
    // DEBUG.logDebug("Find item with: " + tileID);
    // DEBUG.logDebug("New ID: " + tile_id);
    let tileID = store($(".modal-here"), "tile-id");
    let tile_id = $("#tile-id").val();

    socketio.emit("tile_id", {"tile_id": tileID, "new_id": tile_id});
  }

}