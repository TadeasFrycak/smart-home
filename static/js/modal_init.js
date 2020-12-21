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

function initImages(){
  $(".modal-edit-icon").each(function() {
    if (store($(this), 'selected') === true){
      if ($(document.body).hasClass("dark")) {
        $(this).css({"border": "2px solid rgb(232, 93, 71)"});
      }
      else {
        $(this).css({"border": "2px solid rgb(23, 162, 184)"});
      }
    }
    Hammer(this).on("tap", function(elem) {
      // ( > modal_edit_events.js )
      modalEditPreviewImageTap(elem);
    });
  });
}


// /get_modal 
//    > tileId

// /get_add_tile_modal
//    > slideIndex

// /get_edit_modal
//    > tileId

// function addNewTile()
// {
//   socketio.emit("get_add_modal", {"slide_index": swiper.realIndex});
// }

function requestNormalModal($this)
{
  let object_id = store($this.parent(), "id");
  socketio.emit("get_normal_modal", {"tile_id": object_id, "tab_id": sessionStorage.tabID});
}

function requestEditModal($this)
{
  let object_id = store($this.parent(), "id");

  if (store($this.parent(), "type") === "add-new-tile") {
    socketio.emit("get_add_modal", {"slide_index": swiper.realIndex, "tab_id": sessionStorage.tabID});
  }
  else {
    socketio.emit("get_edit_modal", {"tile_id": object_id, "tab_id": sessionStorage.tabID});
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
function initializeModalEditItems(data) {
  $(".modal-edit-item-dropdown").slideUp();
  let tile_id = store($(".modal-here"), "tile-id");
  DEBUG.logDebug("Parent Tile ID: " + tile_id);
  var tile_name = $(".tile[data-id="+tile_id+"]").find(".tile-label").text();
  DEBUG.logDebug("Parent Tile Name :" + tile_name);  
  $("#tile_name").val(tile_name);

  $("#tile-mqtt-path").val("home/" + tile_id);

  $(".modal-edit-item-delete").on("click",function(e){
    // ( > modal_edit_events.js )
    modalEditItemDelete(this);
  });

  $('.modal-item[data-group^="modal-edit-"]').on("value-transmit", function(event) {
    modalEditItemInit(this);
  });

  $(".modal-edit-tile-dynamic-value").on("input",function(e){
    // ( > modal_edit_events.js )
    modalEditTileTextChanged(this);
  });
  
  $("#tile-id").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileIDchanged(this);
  });

  $(".modal-edit-tile-type").on("click", "input",  function() {
    DEBUG.log("Tile type changed");
    // ( > modal_edit_events.js )
    let type_name = $(this).parent().text().trim();
    let tileID = store($(".modal-here"), "tile-id");

    tileTypeChanged(tileID,type_name);
  });
  
  $("#tile_name").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileTitleChanged();
  });

  initImages();

  // Unfocus input 
  $(".unfocus-on-enter").keydown(function(event){
    event.keyCode===13 && $(this).blur();
  });
}

function modalEditItemInit(object) {
  // ( > modal_edit_events.js )
    if (store($(object), "id") === "id") {
      // ( > modal_edit_events.js )
      let itemID = store($(object), "value");
      if (validateID(itemID)) {
        let oldItemID = store($(object), "group").substr(11);
        let tileID = store($(".modal-here"), "tile-id");

        let config = store($(object), "config");
        config["invalid"] = false;
        store($(object), "config", config).trigger("config-receive");

        socketio.emit("modal_item_id", {
          "tile_id": tileID,
          "new_id": itemID,
          "id" : oldItemID
        });
        console.log(store($(object), "group"));
      }
      else {
        let config = store($(object), "config");
        config["invalid"] = true;
        store($(object), "config", config).trigger("config-receive");
      }
    }
    else {
      modalEditItemTextChanged(object);
    }
}