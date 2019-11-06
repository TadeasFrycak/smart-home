$(document).ready(function(){
    console.log("+----------------------------------+");
    console.log("|     IoT Project, version 10.5    |");
    console.log("|     Last modified: 30.10.2019    |");
    console.log("|                                  |");
    console.log("|              © 2019              |");
    console.log("+----------------------------------+");

    // ----------------------------------------------
    // Define some constants variables
    // ----------------------------------------------

    var slider_previous_value = 0;
    var sliders = [];

    var item_unactive_color = "rgb(206, 206, 206)";
    var item_active_color = "rgb(255, 10, 255)";

    // ----------------------------------------------
    // Asynchronous communication
    // ----------------------------------------------

    var socket = io.connect("http://" + document.domain + ":" + location.port + "/acom");

    // Tile
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
                    }

                    else if (previous_tile_state === "OFF" && current_tile_state > 0) {
                        $(this).find(".tileStatus").text("ON"); $(this).toggleClass("tileActive");
                    }
                }
                else if (type_of_item === "percentage") {
                    $(this).find(".tileInputVal").text(msg.v);
                }
            }
        });
    });

    // Slider
    socket.on("slider", function(msg) {
        for (var i = 0; i < sliders.length; i++) {
            var slider_html = sliders[i].selector.offsetParent.outerHTML;
            var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");

            if (slider_detect_id === msg.i) {
                sliders[i].value(msg.v);
            }
        }
    });

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
            }
        });
    });

    $(".tileStatus").each(function() {
        if ($(this).text() === "ON"){
            $(this).parent().parent().toggleClass("tileActive");
        }
    });

    $(document).on('click','img',function(){
        alert("Click event works!");
        });


    // ----------------------------------------------
    // Initialization of objects
    // ----------------------------------------------

    function initModules(value){
        $(".slider").each(function(test) {
            var slider = new hx.Slider(this, {max:100});
            sliders[test] = slider;

            // ----------------------------------------------
            // Event při změně slideru
            // ----------------------------------------------
            slider.on("change", function(data){
                var string = data.html;
                var slider_id = $($.parseHTML(string)).attr("data-id");
                var slider_value = Math.round(data.value);

                if (slider_value !== slider_previous_value) {
                    slider_previous_value = slider_value;
                    $.post( "/slider",
                        {
                            "i": slider_id,
                            "v": slider_value,
                            "id_tile": value
                        },
                        function(result){});
                }
            });
        });

        // ----------------------------------------------
        // Detekuje změnu toggle talčítek uvnitř modalu
        // ----------------------------------------------
        $(document).on('change', '.modal_toggle', function() {
            var object_id = $(this).parent().parent().parent().attr("data-id");
            var object_state = "";
    
            if($(this).prop("checked") === true){
                object_state = "1";
                // checkbox is checked
            }
    
            else if($(this).prop("checked") === false){
                object_state = "0";
                // checkbox is unchecked
            }

            $.post("/toggle",
            {
                "i": object_id,
                "v": object_state,
                "id_tile": value
            },
            function(result){});
    
        });


        $("select").formSelect();
        $(".timepicker").timepicker();


        // ----------------------------------------------
        // Generuje graf
        // ----------------------------------------------
        $(".graphModul").each(function(){
            var chartXaxis = ["1.1.2019","1.2.2019","1.3.2019","1.4.2019", "1.5.2109"];
            var chartData = [12,10,-1,9,1];
            var header = this.getAttribute("data-header");

            var ctx = $(this).children();
            var myChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: chartXaxis,
                    datasets: [{
                        label: header,
                        data: chartData,
                        backgroundColor: [
                            "rgba(255, 99, 132, 0.2)"
                        ],
                        borderColor: [
                            "rgba(255, 99, 132, 1)"
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        });
    }


    // ----------------------------------------------
    // Process data from inputs
    // ----------------------------------------------

    



    $(".tileToggle").each(function(){
        var $this = $(this);
        var mc = new Hammer(this);
        mc.on("tap", function() {
            $this.parent().toggleClass("tileActive");

            var tile_id = $this.parent().attr("data-id");
            var tile_state = 0;
            tile_state = $this.parent().find(".tileStatus").text();

            if (tile_state === "ON") { $this.parent().find(".tileStatus").text("OFF"); tile_state = 0; }
            else if (tile_state === "OFF") { $this.parent().find(".tileStatus").text("ON"); tile_state = 1; }

            $.post("/tile",
            {
                "i": tile_id,
                "v": tile_state
            },
            function(result){});
        });
    });


    
    $(".tileModal").each(function(){
        var $this = $(this);
        var mc = new Hammer(this);
        mc.on("press", function() {
            var object_id = $this.parent().attr("data-id");

            $.post( "/get_modal",
                {
                    "i": object_id
                },

                function(result){
                    // console.log(JSON.parse(result));
                    var json = JSON.parse(result);

                    $(".modalHere").append(json.modal);
                    genModal().style.display = "block";
                    initModules(object_id);
                    var header = tileGetAtributeByName($this.parent(),"tileDescription");
                    $(".modalHeader").text(header);

                    // $('.modal_toggle').prop('checked', true);
                    $(".modal_toggle").each(function(){
                        var x = $(this).parent().parent().parent().attr("data-id");
                        // console.log(x);
                        for (j in json.toggles) {
                            if (x === j) {
                                // console.log()
                                $(this).prop('checked', parseInt(json.toggles[j]));
                            }
                        }
                    });


                    for (var i = 0; i < sliders.length; i++) {
                        var slider_html = sliders[i].selector.offsetParent.outerHTML;
                        var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");

                        for (j in json.sliders) {
                            if (slider_detect_id === j) {
                                sliders[i].value(json.sliders[j]);
                            }
                        }

                    }
                });
        });
    });



    function tileGetAtributeByName(obj, desc){
        return obj.find("." + desc).text();
    }


    // ----------------------------------------------
    // Generate modal window
    // ----------------------------------------------

    function genModal(){
        var modal = document.getElementById("tile-Modal");
        var span = document.getElementsByClassName("close")[0];

        span.onclick = function() {
            modal.style.display = "none";
            $(".modalHere").empty();
        };
        // Close the modal when close button is pressed
        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = "none";
                $(".modalHere").empty();
            }
        };

        return modal;
    }



    // Initialise Swiper
    new Swiper(".swiper-container", {
        pagination: { el: ".swiper-pagination"},
        threshold: "10"
        // allowTouchMove: false,
        // simulateTouch: false,
        // touchStartPreventDefault: true,
        // noSwiping: true,
        // noSwipingClass = "swiper-no-swiping"
        });
});
