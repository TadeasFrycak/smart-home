$(document).ready(function(){
    $(".tile-item").each(function(){
        initializeHammerTile(this);
    });
});

function initializeHammerTile(object) {
    let hammer = new Hammer(object, {cssProps: {userSelect: true}});
    hammer.on("tap", function(el) {
      tapped($(el.target).closest(".tile-item"));
    });

    hammer.on("press", function(el) {
      pressed($(el.target).closest(".tile-item"));
    });
}

function tapped(object) {
  // type of item; [toggle/...]
  let isEditActive = store($(document.body), "is-edit-active");

  // if edit mode is enabled; edit mode
  if (isEditActive === true) {
    console.log("Requested edit modal");
    requestEditModal(object);
  }

  // if edit mode is disabled; normal mode
  else if (isEditActive === false) {
    object.trigger("tap");
  }
}

function pressed(object) {
    let isEditActive = store($(document.body), "is-edit-active");

    // if edit mode is disabled; normal mode
    if (isEditActive === false) {
        requestNormalModal(object);
    }
}

function tileValueTransmit(object) {
  object.on("value-transmit", function() {
    let tileID = store($(this), "id")
    let tileValue = store($(this), "value")
    socketio.emit("tile_value", {"tile_id": tileID, "value": tileValue});
  });
}

tileValueTransmit($(".tile-item"));

