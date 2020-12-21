/*
*
*   modal_edit_events.js
*   - eventy vyvolané interakcí v modalu v normálním režimu
*
*/

$(document).ready(function() {
  $(document.body).on("click", ".doorbird-open-door", function() {
    socketio.emit("doorbird_open_door");
  });
  $(document.body).on("click", ".doorbird-light-on", function() {
    socketio.emit("doorbird_light_on");
  });
  $(document.body).on("click", ".doorbird-take-photo", function() {
    socketio.emit("doorbird_take_photo");
  });
});

function isModalOpen(type=null, tileID=null, modalClosed=false) {
  if ($(document.body).hasClass("modal-open") || modalClosed) {
    let typeGet = store($(".modal-here"), "type");
    let tileIDGet = store($(".modal-here"), "tile-id");

    if (type !== null) {
      if (typeGet === type) {
        if (tileID !== null) {
          if (tileIDGet === tileID) {
            return true;
          }
        }
        else {
          return true;
        }
      }
    }
    else {
      if (tileID !== null) {
        if (tileIDGet === tileID) {
          return true;
        }
      }
      else {
        if (tileIDGet === undefined && typeGet === undefined) {
          return false;
        }

        else if ( tileIDGet === undefined) {
          return {"type": typeGet};
        }

        else {
          return {"type": typeGet, "tile_id": tileIDGet};
        }
      }
    }
  }
  return false;
}