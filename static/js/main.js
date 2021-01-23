// Initialise communication
socketio = io("/com", {
  forceNew: true,
  reconnectionDelay: 100,
  reconnectionDelayMax: 500
});
reconnected = false;

$(document).ready(function(){
//   window.onbeforeunload = function(){
//   return 'Are you sure you want to leave?';
// };

  // setTimeout(function(){
  //   vibrate = navigator.vibrate ? 'vibrate' : navigator.webkitVibrate ? 'webkitVibrate' : null;
  // }, 1000);

  let serverModalOpened = false;

  // Reload page
  socketio.on("reload", function() {
    console.log("Server command: reload");
    location.reload();
  });
  socketio.on("disconnect", function () {
    if (!serverModalOpened) {
      reconnected = true;
      console.log("disconnect");
      document.title = _("Offline") + " | " + _("SH");
      serverModal(_("Offline"), _("Server is now offline. The page will be auto-reloaded after server will be online. If you think that this message is wrong or this is a bug, you can reload page manually."));
    }
  });

  socketio.on("reconnect", function() {
    console.log("Server reconnected! Reloading...");
    location.reload();
  });

  // Asynchronous communication for global notifications
  socketio.on("notify", function(msg) {
    wait = false;
    notify(_(msg.title), _(msg.message), msg.type, msg.delay);
  });

  $(document.body).on("click", ".reload", function() {
    location.reload();
  });
});

function serverModal(header, message, button=_("Reload"), command="reload") {
    $("#my-modal").hide();
    $(".modal-here").empty();
    $(".modal-here").append('<div class="modal fade" id="modal-server" tabindex="-1" role="dialog" aria-hidden="true"> <div class="modal-dialog modal-dialog-centered" role="document"> <div class="modal-content"> <div class="modal-header"> <h5 class="modal-title" id="exampleModalLongTitle">' + header + '</h5> </div> <div class="modal-body">' + message + '</div> <div class="modal-footer"> <button type="button" class="btn btn-danger ' + command +'">' + button + '</button></div></div></div></div>');
    // navigator[vibrate](50);
    $("#modal-server").modal({backdrop: "static", keyboard: false});
}

function notify(title, message, type, delay) {
  // navigator[vibrate](50);
  let width = window.innerWidth;
  let height = window.innerHeight;
  let align;

  if (height > width) {
    align = "center";
  } else {
    align = "right";
  }

  $.notify({
    title: "<strong>" + title +  "</strong>",
    message: message
  }, {
    type: type,
    delay: delay,
    mouse_over: "pause",
    allow_dismiss: true,
    placement: {
      from: "top",
      align: align
    },
    animate: {
      enter: 'animated fadeInDown',
      exit: 'animated fadeOutUp'
    },
    z_index: 2000
  });
}

// TODO sem dát všechno, co je společné s authem - takže socketio inicializaci, fullscreeen, .....