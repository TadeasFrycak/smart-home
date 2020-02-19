$(document).ready(function(){

    var slider_previous_value = 0;
    sliders = [];
    var graphs = [];
    var graphs_id = [];

    function tileGetAtributeByName(obj, desc){
        return obj.find("." + desc).text();
    }


    function sliders_init(value){
        var tile_id = $("#tile_id").val();
        $("#tile_mqtt_path").val("home/" + tile_id);

        sliders = [];

        $(".time-picker-pickie").each(function(test) {
            $(this).timepicki();
            $(this).attr('readonly', 'readonly');
            $(".timepicki-input").attr('readonly', 'readonly');

        });

        $('#tile_id').on('input',function(e){
            var tile_id = $("#tile_id").val();
            var id_of_caller = $(".modalHere").attr("id_of_caller");
            $("#tile_mqtt_path").val("home/" + tile_id);
            $.post( "/tile_id_rwr",
            {
                "tile_id": id_of_caller,
                "new_id": tile_id
            });
            $(".modalHere").attr("id_of_caller",tile_id);
        });

        $('#tile_name').on('input',function(e){
            var tile_name = $("#tile_name").val();
            var tile_id = $("#tile_id").val();
            var id_of_caller = $(".modalHere").attr("id_of_caller");
            $("#tile_mqtt_path").val("home/" + tile_id);
            $.post( "/tile_name_rwr",
            {
                "tile_id": id_of_caller,
                "new_name": tile_name
            });
        });

        $('.modal_edit_item_textbox').on('input',function(e){
            // var tile_id = $("#tile_id").val();
            var id_of_caller = $(".modalHere").attr("id_of_caller");
            // $("#tile_mqtt_path").val("home/" + tile_id);
            // $(".modal_edit_item_textbox").parent().parent().children(".modal_edit_item_textbox_label").text()
            console.log($(this).parent().parent().children(".modal_edit_item_textbox_label").text());
            console.log($(this).val());

            // $.post( "/TODO",
            //     {
            //         "id_of_caller": id_of_caller,
            //         "new_id_value": tile_id
            //     });
        });

        // FS: TODO double sending
        $('.modal_edit_tile_type').on('click',function(e){
            var id_of_caller = $(".modalHere").attr("id_of_caller");
            var type_name = $(this).find(".modal_edit_type_text").text();

            console.log(id_of_caller);
            console.log(type_name);
            $.post( "/tile_type_rwr",
                {
                    "id": id_of_caller,
                    "new_type": type_name
                });
        });

        $('#myModal').on('hidden.bs.modal', function () {
            
        })

        


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

    }



    $(".tileModal").each(function(){
        var $this = $(this);
        var mc = new Hammer(this);
        mc.on("press", function() {
            var object_id = $this.parent().attr("data-id");
            var to_send;
            if (is_edit === false) {
                to_send = 0;
            }
            else if (is_edit === true) {
                to_send = 1;
            }

            $.post( "/get_modal",
                {
                    "i": object_id,
                    "edit": to_send
                },
                

                function(result){

                    var json = JSON.parse(result);
                    $(".modalHere").empty();
                    $(".modalHere").append(json.modal);
                    $('#myModal').modal({
                      keyboard: true
                    })

                    var header = tileGetAtributeByName($this.parent(),"tileDescription");
                    $(".modal-title").text(header);
                    $(".modalHere").attr("id_of_caller",object_id);
                    sliders_init(object_id);

                    $(".modal_items_edit_sortable_item_dropdown").slideUp();

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
});