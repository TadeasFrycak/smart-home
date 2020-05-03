$(document).ready(function(){
  // ----------------------------------------------
  // Receive asynchronous communication
  // ----------------------------------------------

  // Initialise asynchronous communication
  var socket = io.connect("http://" + document.domain + ":" + location.port + "/acom");

  // Asynchronous communication for tile
  socket.on("tile", function(msg) {
    console.log(msg);
    
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
            if (tileStateLast.toLowerCase() == "on" && tileStateCurrent == 0) {
              $(this).find(".tileStatus").text("OFF"); $(this).toggleClass("tileActive");
              $(this).find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");
            }
          
            // Turn tile on
            else if (tileStateLast.toLowerCase() == "off" && tileStateCurrent == 1) {
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

  // Append
  socket.on("graph_append", function(msg) {
    console.log(msg);
    var modal_caller_id = $("#myModal").data("id-of-caller");
    if (modal_caller_id === msg.id_tile) {
      try {
        for (var i = 0; i < graphs_id.length; i++) {
          if (graphs_id[i] == msg.i) {  // Shodné ID
            addGraphData(graphs[i],msg.data_x,msg.data_y);
          }
        }
      }
      catch {
        console.log("acom.js > something failed I guess");
      }
    }
  });

  // Renew
  socket.on("graph_rwr", function(msg) {
    console.log(msg);
    var modal_caller_id = $("#myModal").data("id-of-caller");
    // if (modal_caller_id === msg.id_tile) {
    if (true){
      try {
        for (var i = 0; i < graphs_id.length; i++) {

          if (graphs_id[i] == msg.graph_id) {  // Shodné ID
            console.log("Found my graph");
            // addGraphData(graphs[i],msg.data_x,msg.data_y);
            // addGraphData(graphs[i],msg.data_x,msg.data_y);
            graphs[i].data.datasets[0].data = msg.value.y;
            graphs[i].data.labels = msg.value.x;
            graphs[i].update();
            // websiteChart.update();
          }
        }
      }
      catch {
        console.log("acom.js > something failed I guess");
      }
    }
  });

  // Asynchronous communication for tile_refresh
  socket.on("tile_refresh", function(json) {

    var newID = json.id;
    var tile_id = json.tile_id;
    var pageIndex = json.slide_index;
    console.log("AA");
    console.log(pageIndex);
    var tileS = $(".tile[data-id='"+tile_id+"']");

    var found = 0;
    // Vyhledá stávající Tile
    $(".tile").each(function() {
      var search_id = $(this).attr("data-id");
      if (search_id == newID) found = 1;
    });

    // Pokud našel více shodných Tilů
    if (found > 1) DEBUG.logWarning("! Warning ! more than one ID found! (modal_init.js; ln: 183)");
    // Pokud nenašel stávajíci Tile, vytvoří nový
    // if (found == 0) $(json.tile).insertBefore(".swiper-slide-active .tile_ghost_prefab_class").hide().fadeIn();
    // find page to append refreshed tile
    var pages = []
    $(".swiper-slide").each(function() {
      pages.push(this);
    });

    //$("#wrapper .content:last").before('<div class="content"><div class="subcontent">Third</div></div>');
    if (found == 0) {
      $(pages[pageIndex]).find(".zoomable").find(".add_new_tile_element").before(json.tile).prev().hide().fadeIn();
    }
    // Pokud našel stávající Tile
    else {
      if (json.tile !== "") $(tileS).parent().replaceWith(json.tile);
      else {
        $(tileS).parent().show().fadeOut(function(){
          $(tileS).parent().remove()
        });
      }
    }

    var hammerTime = $(".tile[data-id='"+newID+"']").find(".tileModal")[0];
    var $hammerTime = $(hammerTime);
    var newHammer = new Hammer(hammerTime);

    // Přidělí Hammer "tap"
    initializeTileWithTap(hammerTime);
    // Přidělí Hammer "press"
    initTilePress(newHammer,$hammerTime,0);
  });

  // Reload page
  socket.on("reload", function(msg) {
    location.reload();
  });

  socket.on("connect", function() {
    $(".server-status").text("Online");
  });
  socket.on("disconnect", function() {
    $(".server-status").text("Offline");
    //$(".bcg-real").css({"filter": "grayscale(0.75)", "transition": "filter 2s"});
  });
  socket.on("reconnect", function() {
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
      /*placement: {
		from: "top",
		align: "center"
	  },*/
      animate: {
        enter: "animated fadeInRight", //Down",
        exit: "animated fadeOutRight" //Up"
      },
      z_index: 2000
    });
  });

});



