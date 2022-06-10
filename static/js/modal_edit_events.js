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
    let tileID = isModalOpen().tile_id;

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
  let tileID = isModalOpen().tile_id;
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
  let tileID = isModalOpen().tile_id;
  let newValue = store($(object), "value");
  socketio.emit("modal_item_config", {
    "value_name": itemName,
    "tile_id": tileID,
    "id": store($(object).closest(".modal-edit-item"), "id"),
    "new_value": newValue,
  });
}

// ( < modal_init.js )
function tileTypeChanged(tileID,type_name) {
  DEBUG.logDebug("Change Tile Type to: " + type_name + " (ID: "+tileID+") ");
  socketio.emit("tile_type", {"tile_id": tileID, "new_type": type_name});
}

// ( < modal_init.js )
function tileProtocol(object) {
  DEBUG.log("Tile protocol changed");

  let protocols = store(object, "value");
  let tileID = isModalOpen().tile_id;

  socketio.emit("tile_protocol", {"tile_id": tileID, "protocols": protocols});
}

// ( < modal_init.js )
function modalItemProtocol(object) {
  DEBUG.log("Item protocol changed");
  let protocols = store(object, "value");
  let tileID = isModalOpen().tile_id;
  let itemID = store(object, "id");
  socketio.emit("modal_item_protocol", {"tile_id": tileID, "id": itemID, "protocols": protocols});
}

// ( < modal_init.js )
function modalEditTileTitleChanged() {
  let tile_name = $("#tile_name").val();
  // let tile_id = $("#tile-id").val();
  let tileID = isModalOpen().tile_id;

  // $("#tile-mqtt-path").val("home/" + tile_id);

  socketio.emit("tile_label", {"tile_id": tileID, "new_label": tile_name});
}
