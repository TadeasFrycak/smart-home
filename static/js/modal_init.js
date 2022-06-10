/*
*
*   modal_init.js
*   - inicializuje Itemy v modalovém okně v normálním režimu
*
*/

$(document).ready(function(){
});

graphs = [];
graphs_id = [];

function tileGetAtributeByName(obj, desc){
  return obj.find("." + desc).text();
}

function initTilePress(hammer, $this, add_new_item)
{
  hammer.on("press", function() {
    // ( > modal_init.js )
    // RequestModal($this, add_new_item);
    let isEditActive = store($(document.body), "is-edit-active");
    if (isEditActive === false)
    {
      RequestModal($this, add_new_item);
    }
  });
}

function initTileTap(hammer, $this, add_new_item)
{
  hammer.on("tap", function() {
    // ( > modal_init.js )
    // console.log("Tapped!");
    let isEditActive = store($(document.body), "is-edit-active");
    if (isEditActive === true)
    {
      RequestModal($this, add_new_item);
      console.log("Requested modal!");
    }
    else if (store($($this), "type") === "toggle"){
      tappedOnToggle($this)
    }

  });
}

function requestNormalModal(object)
{
  let tileID = store(object, "id");
  socketio.emit("get_normal_modal", {"tile_id": tileID, "tab_id": sessionStorage.tabID});
}

function requestEditModal(object)
{
  let tileID = store(object, "id");

  if (object.length === 0) {
    socketio.emit("get_add_modal", {"slide_index": swiper.realIndex, "tab_id": sessionStorage.tabID});
  }
  else {
    socketio.emit("get_edit_modal", {"tile_id": tileID, "tab_id": sessionStorage.tabID});
  }
  
}

function modalDynamicValueSend(object) {
  // let attr = $(this).parent().parent().parent().attr("data-static");
    // if (typeof attr !== typeof undefined && attr !== false){
    //   socketio.emit("tile_value", {"value": {[toggleID]: toggleState}, "tile_id": tileID});
    // }
    // else{
    let value = store($(object), "value");

      socketio.emit("modal_item_value", {"id": store($(object), "id"), "value": value,
        "tile_id": store($(".modal-here"), "tile-id"), "type": store($(object), "type")});
    // }
}

function initializeTileDynamic() {
  $('.modal-item[data-group="tile-dynamic"]').on("value-transmit", function() {
    socketio.emit("tile_config", {
      "value_name": store($(this), "id"),
      "tile_id": store($(".modal-here"), "tile-id"),
      "value": store($(this), "value")
    });
  });
}

function tileProtocolInit(object) {
  let value = store($(object), "value");
  let valueName = store($(object), "id");
  let protocol = store($(object).closest("fieldset"), "type");
  let tileID = store($(object).closest("fieldset"), "id")

  socketio.emit("tile_protocol_values", {
      "value_name": valueName,
      "protocol": protocol,
      "tile_id": tileID,
      "value": value
    });
}

function modalItemProtocolInit(object) {
  let value = store($(object), "value");
  let valueName = store($(object), "id");
  let protocol = store($(object).closest("fieldset"), "type");
  let itemID = store($(object).closest("fieldset"), "id")
  let tileID = isModalOpen().tile_id;
  socketio.emit("modal_item_protocol_values", {
      "value_name": valueName,
      "protocol": protocol,
      "id": itemID,
      "tile_id": tileID,
      "value": value
    });
}

function initializeModalEditItems(data) {
  $(".modal-edit-item-dropdown").slideUp();
  let tile_id = store($(".modal-here"), "tile-id");
  DEBUG.logDebug("Parent Tile ID: " + tile_id);

  $(".modal-edit-item-delete").on("click",function(e){
    // ( > modal_edit_events.js )
    modalEditItemDelete(this);
  });

  $('.modal-item[data-group^="modal-edit-"]').on("value-transmit", function() {
    modalEditItemTextChanged(this);
  });

  $('.modal-item[data-group="protocol-tile"]').on("value-transmit", function() {
    tileProtocolInit(this);
  });

  $('.modal-item[data-group^="protocol-item-"]').on("value-transmit", function() {
    modalItemProtocolInit(this);
  });

  if (!$.trim($(".tile-values-wrapper").html())) {
    $("#tile-dynamic-values").hide()
  }
  initializeTileDynamic();

  $('.modal-item[data-group="tile"][data-id="type"]').on("value-transmit", function() {
    DEBUG.log("Tile type changed");
    // ( > modal_edit_events.js )
    let type_name = store(this, "value");
    let tileID = isModalOpen().tile_id;

    tileTypeChanged(tileID,type_name);
  });

  $('.modal-item[data-group="tile"][data-id="protocol-btn"]').on("value-transmit", function() {
    tileProtocol(this);
  });

  $('.modal-item[data-group="item-protocol-btn"]').on("value-transmit", function() {
    modalItemProtocol(this);
  });

  $("#tile_name").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileTitleChanged();
  });

  // Unfocus input
  $(".unfocus-on-enter").keydown(function(event){
    event.keyCode===13 && $(this).blur();
  });
}
