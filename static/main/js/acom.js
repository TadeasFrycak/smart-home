$(document).ready(function(){
  // ----------------------------------------------
  // Receive asynchronous communication
  // ----------------------------------------------

  // Initialise asynchronous communication
  var socket = io.connect("http://" + document.domain + ":" + location.port + "/acom");

  // Asynchronous communication for tile
  socket.on("tile", function(msg) {
    // If I am not sender
    if (msg.device_number != deviceNumber) {
      // Test each tile on the page
      $(".tile").each(function() {
        var tileID = $(this).attr("data-id");

        // If tile ID is same
        if (tileID === msg.id) {
          var tileType = $(this).attr("data-type");
        
          // Tile type is toggle
          if (tileType === "toggle") {
            var tileStateLast = $(this).find(".tileStatus").text();
            var tileStateCurrent = msg.value;

            // Turn tile off
            if (tileStateLast === "ON" && tileStateCurrent == "OFF") {
              $(this).find(".tileStatus").text("OFF"); $(this).toggleClass("tileActive");
              $(this).find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");
            }
          
            // Turn tile on
            else if (tileStateLast === "OFF" && tileStateCurrent == "ON") {
              $(this).find(".tileStatus").text("ON"); $(this).toggleClass("tileActive");
              $(this).find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
            }
          }
        
          // Tile type is percentage
          else if (tileType === "percentage") {
            $(this).find(".tileInputVal").text(msg.v);
          }
        }
      });
    }
  });

  // Asynchronous communication for modal slider
  socket.on("slider", function(msg) {
    // If I am not sender
    if (msg.device_number != deviceNumber) {
      var tileID = $(".modal-here").attr("id_of_caller");
      // If tile ID is same
      if (tileID === msg.tile_id) {
        // For each sliders
        for (var i = 0; i < sliders.length; i++) {
          var sliderHTML = sliders[i].selector.offsetParent.outerHTML;
          var sliderID = $($.parseHTML(sliderHTML)).attr("data-id");
          // If slider ID is same
          if (sliderID === msg.id) {
            sliders[i].value(msg.value);
          }
        }
      }
    }
  });

  // Asynchronous communication for modal toggle
  socket.on("toggle", function(msg) {
    var tileID = $(".modal-here").attr("id_of_caller");

    // If tile ID is same
    if (tileID === msg.tile_id) {
      $(".modal_toggle").each(function(){
        var toggleID = $(this).parent().parent().parent().attr("data-id");

        // If toggle ID is same
        if (toggleID === msg.id) {
          $(this).prop('checked', parseInt(msg.value));
        }
      });
    }
  });

  // Reload page
  socket.on("reload", function(msg) {
    location.reload();
  });

  // Asynchronous communication for global notifications
  socket.on("notify", function(msg) {
    $.notify({
      title: "<strong>" + msg.title +  "</strong>",
      message: msg.message
    }, {
      type: msg.type,
      delay: 5000,
      mouse_over: "pause",
      allow_dismiss: true,
      animate: {
        enter: "animated fadeInRight",
        exit: "animated fadeOutRight"
      },
      z_index: 2000
    });
  });
});
