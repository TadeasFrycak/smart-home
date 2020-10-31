$(document).ready(function(){
//   window.onbeforeunload = function(){
//   return 'Are you sure you want to leave?';
// };
  //JUST AN EXAMPLE, PLEASE USE YOUR OWN PICTURE!
// var imageAddr = "/img/backgrounds/original/IMG_1460.JPG";
// var downloadSize = 7285568; //bytes
//
// function ShowProgressMessage(msg) {
//   alert(msg)
//     if (terminal) {
//         if (typeof msg == "string") {
//             terminal.log(msg);
//         } else {
//             for (var i = 0; i < msg.length; i++) {
//                 terminal.log(msg[i]);
//             }
//         }
//     }
//
//     var oProgress = document.getElementById("progress");
//     if (oProgress) {
//         var actualHTML = (typeof msg == "string") ? msg : msg.join("<br />");
//         oProgress.innerHTML = actualHTML;
//     }
// }
//
// function InitiateSpeedDetection() {
//     // ShowProgressMessage("Loading the image, please wait...");
//     window.setTimeout(MeasureConnectionSpeed, 1);
// };
//
// if (window.addEventListener) {
//     window.addEventListener('load', InitiateSpeedDetection, false);
// } else if (window.attachEvent) {
//     window.attachEvent('onload', InitiateSpeedDetection);
// }
//
// function MeasureConnectionSpeed() {
//     var startTime, endTime;
//     var download = new Image();
//     download.onload = function () {
//         endTime = (new Date()).getTime();
//         showResults();
//     }
//
//     download.onerror = function (err, msg) {
//         ShowProgressMessage("Invalid image, or error downloading");
//     }
//
//     startTime = (new Date()).getTime();
//     var cacheBuster = "?nnn=" + startTime;
//     download.src = imageAddr + cacheBuster;
//
//     function showResults() {
//         var duration = (endTime - startTime) / 1000;
//         var bitsLoaded = downloadSize * 8;
//         var speedBps = (bitsLoaded / duration).toFixed(2);
//         var speedKbps = (speedBps / 1024).toFixed(2);
//         var speedMbps = (speedKbps / 1024).toFixed(2);
//         ShowProgressMessage([
//             "Your connection speed is:",
//             speedBps + " bps",
//             speedKbps + " kbps",
//             speedMbps + " Mbps"
//         ]);
//     }
// }
  // Initialise communication
  socketio = io("/com");
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
      console.log("disconnect");
      document.title = _("Offline") + " | " + _("SH");
      serverModal("Offline", "Server is now offline. The page will be auto-reloaded after server will be online. If you think that this message is wrong or this is a bug, you can reload page manually.");
    }
  });

  socketio.on("restart", function () {
    console.log("restart");
    serverModalOpened = true;
    document.title = _("Restarting") + " | " + _("SH");
    serverModal("Restarting", "Server is now restarting. If the server will not turn on automatically within a minute, please refresh the page manually");
  });

  socketio.on("shutdown", function () {
    console.log("shutdown");
    serverModalOpened = true;
    document.title = _("Turned off") + " | " + _("SH");
    serverModal("Turned off", "Server was turned off. Please, reload the page when you turn on the server.");
  });

  socketio.on("reconnect", function() {
    console.log("Server reconnected! Reloading...");
    location.reload();
  });

  // Asynchronous communication for global notifications
  socketio.on("notify", function(msg) {
    notify(msg.title, msg.message, msg.type, msg.delay);
  });

  $("body").on("click", ".reload", function() {
    location.reload();
  });
});

function serverModal(header, message) {
    $("#myModal").hide();
    $(".modal-here").empty();
    $(".modal-here").append('<div class="modal fade" id="modal-server" tabindex="-1" role="dialog" aria-hidden="true"> <div class="modal-dialog modal-dialog-centered" role="document"> <div class="modal-content"> <div class="modal-header"> <h5 class="modal-title" id="exampleModalLongTitle">' + header + '</h5> </div> <div class="modal-body">' + message + '</div> <div class="modal-footer"> <button type="button" class="btn btn-danger reload">Reload</button></div></div></div></div>');
    // navigator[vibrate](50);
    $("#modal-server").modal({backdrop: "static", keyboard: true});
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