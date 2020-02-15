$(document).ready(function(){
    console.log("+----------------------------------+");
    console.log("|     IoT Project, version 10.6    |");
    console.log("|     Last modified: 30.10.2019    |");
    console.log("|                                  |");
    console.log("|              © 2019              |");
    console.log("+----------------------------------+");

    // ----------------------------------------------
    // Define some constants variables
    // ----------------------------------------------

    // Grid demo
        

    new Sortable(gridDemo, {
        animation: 150,
        ghostClass: 'blue-background-class'
    });
        // $("#gridDemo").each(function() {
        // });


    var slider_previous_value = 0;
    var sliders = [];
    var graphs = [];
    var graphs_id = [];
    var device_number = Math.round(Math.random() * 1000);

    var item_unactive_color = "rgb(206, 206, 206)";
    var item_active_color = "rgb(255, 10, 255)";

    var GaugesByID = [];
    function createRadGauge(t,e,a,n){function r(t,e,a,n){return{x:t+a*Math.cos(n),y:e+a*Math.sin(n)}}function s(t,e,a,n,s,o){var d=r(t,e,a,-Math.PI),l=r(t,e,a,-Math.PI*(1-1/(o-s)*(n-s))),i=["M",d.x,d.y,"A",a,a,0,0,1,l.x,l.y].join(" ");return i}var o='<svg class="rGauge" viewBox="0 0 200 145"><path class="rGauge-base" id="'+t+'_base" stroke-width="30" /><path class="rGauge-progress" id="'+t+'_progress" stroke-width="30" stroke="#1565c0" /><text class="rGauge-val" id="'+t+'_val" x="100" y="105" text-anchor="middle"></text><text class="rGauge-min-val" id="'+t+'_minVal" x="40" y="125" text-anchor="middle"></text><text class="rGauge-max-val" id="'+t+'_maxVal" x="160" y="125" text-anchor="middle"></text></svg>';document.getElementById(t).innerHTML=o,document.getElementById(t+"_base").setAttribute("d",s(100,100,60,1,0,1)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,e,e,a)),document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var d={setVal:function(r){return r=Math.max(e,Math.min(r,a)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,r,e,a)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),d},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("stroke",e),d}};return d}function createVerGauge(t,e,a,n){var r='<svg class="vGauge" viewBox="0 0 145 145"><rect class="vGauge-base" id="'+t+'_base" x="30" y="25" width="30" height="100"></rect><rect class="vGauge-progress" id="'+t+'_progress" x="30" y="25" width="30" height="0" fill="#1565c0"></rect><text class="vGauge-val" id="'+t+'_val" x="70" y="80" text-anchor="start"></text><text class="vGauge-min-val" id="'+t+'_minVal" x="70" y="125"></text><text class="vGauge-max-val" id="'+t+'_maxVal" x="70" y="30" text-anchor="start"></text></svg>';document.getElementById(t).innerHTML=r,document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var s={setVal:function(r){r=Math.max(e,Math.min(r,a));var o=100/(a-e)*(r-e);return document.getElementById(t+"_progress").setAttribute("height",o),document.getElementById(t+"_progress").setAttribute("y",25+(100-o)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),s},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("fill",e),s}};return s}

    // createRadGauge("ABCD",0,100,"l").setVal(25);

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
        try {
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
        }
        catch
        {console.log("chybvole");}
    });

    // Toggle
    socket.on("toggle", function(msg) {
        // var audio = new Audio('static/birds.mp3');
        // audio.play();
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

    $(".tileStatus").each(function() {
        if ($(this).text() === "ON"){
            $(this).parent().parent().toggleClass("tileActive");
        }
    });

    $(document).on("click","img",function(){
        window.location.href = "edit";
    });

    $('body').on('hidden.bs.modal', '.modal', function () {
        $("#myModal").remove();
        $(".modalHere").html("");
    });

    $(".tile_gauge").each(function(test) {
            
        var target_id = $(this).attr("data-target_id")
        var min_val = $(this).attr("data-min_val")
        var max_val = $(this).attr("data-max_val")
        var suffix = $(this).attr("data-suffix")
        var color = $(this).attr("data-color")
        var target_value = $(this).attr("data-target_value")

        createRadGauge(target_id,min_val,max_val,suffix).setColor(color).setVal(target_value);
    });




    // ----------------------------------------------
    // Initialization of objects
    // ----------------------------------------------

    function initModules(value){
        

        sliders = [];
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
                            "id_tile": value,
                            "device_number": device_number
                        },
                        function(result){});
                }
            });

        });

        // ----------------------------------------------
        // Detekuje změnu toggle talčítek uvnitř modalu
        // ----------------------------------------------
        // $(document).on('change', '.modal_toggle', function() {
        $('body').on('change', '.modal_toggle', function(e){
            var object_id = $(this).parent().parent().parent().attr("data-id");
            var object_state = "";
            e.stopPropagation();
            e.stopImmediatePropagation();

            if($(this).prop("checked") === true){
                object_state = "1";
                // checkbox is checked
            }

            else if($(this).prop("checked") === false){
                object_state = "0";
                // checkbox is unchecked
            }

            value = $("#myModal").data("id-of-caller");
            
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


        
    }


    // ----------------------------------------------
    // Process data from inputs
    // ----------------------------------------------
    $(".tileToggle").each(function(){
        var $this = $(this);
        var mc = new Hammer(this);
        mc.on("tap", function() {
            // $this.parent().toggleClass("tileActive");

            var tile_id = $this.parent().attr("data-id");
            var tile_state = 0;
            tile_state = $this.parent().find(".tileStatus").text();
            var tile_name = $this.parent().find(".tileDescription").text();
            $('.device').css('display','block');

            $("#itemName").val(tile_name);
            $("#itemName").attr("data-caller",tile_id);
            var path = "home/" + tile_id
            $("#MQQT_Path").val(path);
            $("#Tile_id").val(tile_id);
            

        });
    });



    $(".tileModal").each(function(){
        var $this = $(this);
        var mc = new Hammer(this);
        mc.on("press", function() {
            // document.getElementsByClassName(".modal")

            var object_id = $this.parent().attr("data-id");

            $.post( "/get_modal",
                {
                    "i": object_id
                },

                function(result){

                    var json = JSON.parse(result);

                    $(".modalHere").append(json.modal);
                    $('#myModal').modal('show');
                    var header = tileGetAtributeByName($this.parent(),"tileDescription");
                    $(".modal-title").text(header);
                    $("#myModal").data("id-of-caller",object_id);
                    initModules(object_id);

                    // ----------------------------------------------
                    // Generuje graf
                    // ----------------------------------------------                    
                    $(".apex-graph").each(function(){
                        for (k in json.graphs){
                            if (k == $(this).attr("data-id")){ // Nasel graf sse setejným ID

                                var myData = json.graphs[k].values;
                                var graph_name = json.graphs[k].label;
                                var x_min = json.graphs[k].max_min.x.min;
                                var x_max = json.graphs[k].max_min.x.max;
                                var y_min = json.graphs[k].max_min.y.min;
                                var y_max = json.graphs[k].max_min.y.max;
                                
                                var options = {
                                    series: [{
                                        name: graph_name,
                                        data: myData
                                    }],
                                    chart: {
                                        id: k+'chart2',
                                        type: 'line',
                                        height: 230,
                                        toolbar: {
                                            autoSelected: 'pan',
                                            show: false
                                        }
                                    },
                                    colors: ['#546E7A'],
                                    stroke: {
                                        width: 7,
                                        curve: 'smooth'
                                    },
                                    dataLabels: {
                                        enabled: false
                                    },
                                    fill: {
                                            type: 'gradient',
                                            gradient: {
                                            shade: 'dark',
                                            gradientToColors: [ '#FDD835'],
                                            shadeIntensity: 1,
                                            type: 'horizontal',
                                            opacityFrom: 1,
                                            opacityTo: 1,
                                            stops: [0, 100, 100, 100]
                                            },
                                        },
                                        markers: {
                                            size: 4,
                                            colors: ["#FFA41B"],
                                            strokeColors: "#fff",
                                            strokeWidth: 2,
                                            hover: {
                                            size: 7,
                                            }
                                        },
                                    xaxis: {
                                        type: 'datetime',
                                    },
                                    yaxis: {
                                        title: {
                                            text: graph_name,
                                            }
                                    }
                                };
                                
                                var chart = new ApexCharts(document.querySelector("#"+k), options);
                                chart.render();
                                
                                var optionsLine = {
                                    series: [{
                                        data: myData
                                    }],
                                    chart: {
                                        id: k+'chart1',
                                        height: 130,
                                        type: 'area',
                                        brush: {
                                            target: k+'chart2',
                                            enabled: true
                                        },
                                        selection: {
                                            enabled: true,
                                            xaxis: {
                                                min: x_min,
                                                max: x_max
                                            }
                                        },
                                    },
                                    
                                    colors: ['#FFA41B'],
                                    fill: {
                                        type: 'gradient',
                                        gradient: {
                                            opacityFrom: 0.91,
                                            opacityTo: 0.1,
                                        }
                                    },
                                    xaxis: {
                                        type: 'datetime',
                                        tooltip: {
                                            enabled: false
                                        }
                                    },
                                    yaxis: {
                                        tickAmount: 2,
                                        min: y_min,
                                        max: y_max,
                                        
                                    }
                                };
                                
                                var chartLine = new ApexCharts(document.querySelector("#"+k+"_brush"), optionsLine);
                                chartLine.render();
                            }
                        }
                    });


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
                        var test = sliders[i].selector;
                        var slider_html = sliders[i].selector.parentElement.outerHTML;
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

function addGraphData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function removeGraphData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}


// Initialise Swiper
//var swiper = new Swiper(".swiper-container", {
//    pagination: {
//        el: ".swiper-pagination",
//        dynamicBullets: true,
//        },
//    threshold: "10",
    // allowTouchMove: false,
    // simulateTouch: false,
    // touchStartPreventDefault: true,
    // noSwiping: true,
    // noSwipingClass = "swiper-no-swiping"
    //  });

    var swiper = new Swiper('.swiper-container', {
    navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
    },
    allowTouchMove: false,
});

function pageName_update() {
    var name = $('.swiper-slide')[swiper.realIndex].innerHTML.split("<div class=\"swipe-header\">")[1].split("</div>")[0].trim();
    $("#pageName").val(name);
}
    swiper.on("slideChange", function() {
    pageName_update();
});

pageName_update();
jQuery("#pageName").on("input", function()
    {
        var text = $("#pageName").val();
        $(".swiper-slide-active").find(".swipe-header").text(text);
        console.log(text);
        $.post("/title",
            {
                "index": swiper.realIndex,
                "v": text
            },
            function(result){});
});

$("#btn-addPage").on('click', function(event) {
    swiper.appendSlide("<div class='swiper-slide'><div class='swipe-header'>Bez názvu</div><div class='swipe-content'><div class='end-block'></div></div></div>");
    swiper.slideTo(swiper.slides.length-1, 1000);
    $.post("/append_slide",
            {
                "index": swiper.slides.length-1,
                "v": "Bez názvu"
            },
            function(result){});
});

$("#btn-deletePage").on('click', function(event) {
    swiper.removeSlide(swiper.realIndex);

    $.post("/remove_slide",
            {
                "index": swiper.realIndex
            },
            function(result){});
});

$("#opt-percentage").on('click', function(event) {
    console.log("asdjkfh");
    var caller = $("#opt-percentage").attr("data-caller");
    $.post("/change_tile",
            {
                "i": caller,
                "type": "percentage"
            },
            function(result){});
});

$("#opt-toggle").on('click', function(event) {
    console.log("asdjkfh");
    var caller = $("#opt-toggle").attr("data-caller");
    $.post("/change_tile",
            {
                "i": caller,
                "type": "toggle"
            },
            function(result){});
});

$("#opt-tile").on('click', function(event) {
    $(".edit-tile").css("display","block");
    $(".edit-modal").css("display","none");
});

$(".edit_list_source_item").on('click', function(event) {
    if ($(this).parent().attr("data-destination") == "true")
    {
        if ($('.edit_list_dropdown:hover').length == 0) {
            $(this).find(".edit_list_dropdown").toggleClass("edit_list_dropdown_show");
        }
    }
});


$("#opt-modal").on('click', function(event) {
    $(".edit-modal").css("display","block");
    $(".edit-tile").css("display","none");
    new Sortable(edit_list_source, {
        group: {
            name: 'shared',
            pull: 'clone',
            put: false // Do not allow items to be put into this list
        },
        animation: 150,
        sort: false // To disable sorting: set sort to false
    });


    
    new Sortable(edit_list_dest, {
        group: 'shared',
        animation: 150,
        ghostClass: 'blue-background-class'
    });
});



jQuery("#itemName").on("input", function()
{
    var caller = $("#itemName").attr("data-caller");
    var text = $(this).val();

    // alert($("#" + caller).html());
    $(".tile[data-id="+caller+"]").find(".tileDescription").text(text);
    $.post("/tile_title",
            {
                "i": caller,
                "name": text
            },
            function(result){});
    });
});



