$(document).ready(function(){
    // ----------------------------------------------
    // Asynchronous communication
    // ----------------------------------------------

    // Initialise
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/acom");

    // Asynchronous communication for tile
    socket.on("tile", function(msg) {
        $(".tile").each(function() {
            var attribute_of_current_item = $(this).attr("data-id");
            if (attribute_of_current_item === msg.i)
            {
                var type_of_item = $(this).attr("data-type");

                if (type_of_item === "toggle"){
                    var previous_tile_state = $(this).find(".tileStatus").text();
                    var current_tile_state = msg.v;
                    // console.log(current_tile_state);
                    if (previous_tile_state === "ON" && current_tile_state == 0) {
                        $(this).find(".tileStatus").text("OFF"); $(this).toggleClass("tileActive");
                        $(this).find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");
                    }
                    else if (previous_tile_state === "OFF" && current_tile_state > 0) {
                        $(this).find(".tileStatus").text("ON"); $(this).toggleClass("tileActive");
                        $(this).find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
                    }
                }
                else if (type_of_item === "percentage") {
                    $(this).find(".tileInputVal").text(msg.v);
                }
            }
        });
    });

    // Asynchronous communication for  slider
    socket.on("slider", function(msg) {
        //try {
            var modal_caller_id = $("#myModal").data("id-of-caller");
            if (modal_caller_id === msg.id_tile)
            {
                for (var i = 0; i < sliders.length; i++) {
                    var slider_html = sliders[i].selector.offsetParent.outerHTML;
                    var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");

                    if (slider_detect_id === msg.i) {
                        if (msg.device_number != device_number) {
                            sliders[i].value(msg.v);
                        }
                    }
                }
            }
        //}
        //catch
        //{console.log("Chyba Tade !");}
    });

    // Asynchronous communication for toggle
    socket.on("toggle", function(msg) {
        var modal_caller_id = $("#myModal").data("id-of-caller");
        if (modal_caller_id === msg.id_tile)
        {
            $(".modal_toggle").each(function(){
                var x = $(this).parent().parent().parent().attr("data-id");
                if (x === msg.i) {
                    $(this).prop('checked', parseInt(msg.v));
                }
            });
        }
    });


    // Asynchronous communication for graphs
    socket.on("graphs", function(msg) {
        console.log(msg);
        var modal_caller_id = $("#myModal").data("id-of-caller");
        if (modal_caller_id === msg.id_tile)
        {
            try{
                for (var i = 0; i < graphs_id.length; i++) {
                    if (graphs_id[i] == msg.i) // Shodné ID
                    {
                        addGraphData(graphs[i],msg.data_x,msg.data_y);
                    }
                }
            }
            catch{console.log("fail");}
        }
    });

    // Asynchronous communication for notifications
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