/*
*
*   modal_init.js
*   - inicializuje Itemy v modalovém okně v normálním režimu
*
*/

$(document).ready(function(){
});

graphs = [];
graphs_id = [];

function tileGetAtributeByName(obj, desc){
  return obj.find("." + desc).text();
}

function initTilePress(hammer, $this, add_new_item)
{
  hammer.on("press", function() {
    // ( > modal_init.js )
    RequestModal($this, add_new_item);
  });
}

function initTileTap(hammer, $this, add_new_item)
{
  hammer.on("tap", function() {
    // ( > modal_init.js )
    RequestModal($this, add_new_item);
  });
}

function initImages(){
  $(".modal-edit-select-img").each(function() {
    var attr = $(this).attr('checked');
    if (typeof attr !== typeof undefined && attr !== false) {
      $(this).css({"border": "2px solid rgb(23, 162, 184)"});
    }
    Hammer(this).on("tap", function(elem) {
      // ( > modal_edit_events.js )
      modalEditPreviewImageTap(elem);
    });
  });
}

function RequestModal($this, add_new_item)
{
    var object_id = $this.parent().attr("data-id");

    var isEditActive = $("body").attr("is_edit_active");

    var normalOrEditRequest = 0;
    if (isEditActive === "true") normalOrEditRequest = 1;

    DEBUG.logLabeled("Is edit activated",normalOrEditRequest);
    DEBUG.logLabeled("Add",add_new_item);
    DEBUG.logLabeled("Page index",swiper.realIndex);
    DEBUG.logLabeled("ID of current Tile",object_id);

    // Request modal - Normal / Edit
    $.post("/get_modal", {
      "id": object_id,
      "edit": normalOrEditRequest,
      "add": add_new_item,
      "slide_index": swiper.realIndex
    }, 
    function(result){
        // ( > modal_init.js )
        initializeModal(result, $this);
        $(".bcg-real").css({"transform": "scale(1.2)", "transition": "all 0.75s"});
        $('#myModal').on('hide.bs.modal', function () {
          $(".bcg-real").css({"transform": "scale(1)", "transition": "all 0.75s"});
        })

        // $(".swipe-body").css({"filter": "blur(1.8px) grayscale(75%)", "transition": "filter 1s"});
        // $(".bcg-real").css({"filter": "blur(1.8px) grayscale(75%)", "transition": "filter 1s"});
        // $(".bcg-image").css({"filter": "blur(1.8px) grayscale(75%)", "transition": "filter 1s"});
    });
}

function initializeModal(result, $this)
{
    var object_id = $this.parent().attr("data-id");
    var json = JSON.parse(result);
    $(".modal-here").empty();
    $(".modal-here").append(json.modal);

    $("#myModal").modal({ keyboard: true })

    // Event při zavření modalu
    $("#myModal").on("hidden.bs.modal", function () {
      // $(".swipe-body").css({"filter": "none", "transition": "filter 0.5s"});
      // $(".bcg-real").css({"filter": "none", "transition": "filter 0.5s"});
      // $(".bcg-image").css({"filter": "none", "transition": "filter 0.5s"});
    })

    var header = tileGetAtributeByName($this.parent(),"tileDescription");
    $(".modal-title").text(header);
    $(".modal-here").attr("id_of_caller", object_id);

    if (object_id === undefined) {
      tile_id = $("#tile-id").val();
      console.log(tile_id);
      $(".modal-here").attr("id_of_caller", tile_id);
    }

    $(".modal_items_edit_sortable_item_dropdown").slideUp();
    // ( > modal_init.js )
    initializeAllItemsWithinModal(json,object_id);
}

function initializeAllItemsWithinModal(json,value)
{
  /*
  *   V normálním režimu   
  */

  console.log(json);
  console.log(value);
 
  $(".date-range-picker-input").each(function(){

    var rangePickerId = $(this).attr("id");

    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
      $(".date-range-picker-input[id="+rangePickerId+"]").find("span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
      var id_of_caller = $(".modal-here").attr("id_of_caller");
      var pair_id = $(".date-range-picker-input[id="+rangePickerId+"]").parent().attr("data-pair");

      $.post("/datarangepicker", {
        "pair_id" : pair_id,
        "tile_id" : id_of_caller,
        "id": rangePickerId,
        "start_value": moment(start).format("YYYY-MM-DD hh:mm:ss"),
        "end_value": moment(end).format("YYYY-MM-DD hh:mm:ss")
      });
    }

    $(".date-range-picker-input[id="+rangePickerId+"]").daterangepicker({
        timePicker: true,
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        locale: {
          format: 'M/DD hh:mm A'
        }
    }, cb);

    // cb(start, end);

    for (var k in json.daterangepickers){
      if (k == rangePickerId){ 
        var dateStart = moment(json.daterangepickers[k].start).format('MMMM D, YYYY');
        var dateEnd = moment(json.daterangepickers[k].end).format('MMMM D, YYYY');
        $(".date-range-picker-input[id="+rangePickerId+"]").find("span").html(dateStart + ' - ' + dateEnd);
      }
    }
      
    

  });

  $(".graphModul").each(function(){
    for (k in json.graphs){
      if (k == $(this).attr("data-id")){ // Nasel graf sse setejným ID
        var ctx = $(this).children();
        var new_chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: json.graphs[k].data_x,
            datasets: [{
                label: $(this).attr("data-header"),
                borderColor: 'rgb(255, 99, 132)',
                data: json.graphs[k].data_y
            }]
          },
          options: {
            scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
          }}
        });
        graphs[graphs.length] = new_chart;
        graphs_id[graphs_id.length] =  $(this).attr("data-id");
        }
    }


});

  // Generuje graf
  $(".apex-graph").each(function(){
    for (k in json.graphs){
        if (k == $(this).attr("data-id")) {  // Nasel graf sse setejným ID
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
            id: k+"chart2",
            type: "line",
            height: 230,
            toolbar: {
                autoSelected: "pan",
                show: false
            }
            },
            colors: ["#546E7A"],
            stroke: {
            width: 7,
            curve: "smooth"
            },
            dataLabels: {
            enabled: false
            },
            fill: {
            type: "gradient",
            gradient: {
                shade: "dark",
                gradientToColors: ["#FDD835"],
                shadeIntensity: 1,
                type: "horizontal",
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
            type: "datetime",
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
            id: k+"chart1",
            height: 130,
            type: "area",
            brush: {
                target: k+"chart2",
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
            colors: ["#FFA41B"],
            fill: {
            type: "gradient",
            gradient: {
                opacityFrom: 0.91,
                opacityTo: 0.1,
            }
            },
            xaxis: {
            type: "datetime",
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
  
  // Inicializace sliderů
  sliders = [];
  $(".slider").each(function(test) {
    var slider = new hx.Slider(this, {max:100});
    sliders[test] = slider;

    // Event při změně slideru
    slider.on("change", function(data){
      var string = data.html;
      var slider_id = $($.parseHTML(string)).attr("data-id");
      var slider_value = Math.round(data.value);

      $.post( "/slider", {
        "id": slider_id,
        "value": slider_value,
        "tile_id": value,
        "device_number": deviceNumber
      }, function(result){});

    });
  });
  
  for (var i = 0; i < sliders.length; i++) {
    // var test = sliders[i].selector;
    var slider_html = sliders[i].selector.parentElement.outerHTML;
    var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");

    for (j in json.sliders) {
      if (slider_detect_id === j) {
        sliders[i].value(json.sliders[j]);
      }
    }
  }

  // Inicializování TimePickie
  $(".time-picker-pickie").each(function() {
    $(this).timepicki({show_meridian:false, max_hour_value:23});
    $(this).attr("readonly", "readonly");
    $(".timepicki-input").attr("readonly", "readonly");
  });

  /*
  *   V editovacím režimu   
  */

  // V edit-modalu

  var tile_id = $("#tile-id").val();
  DEBUG.logDebug("Parent Tile ID: " + tile_id);
  var tile_name = $(".tile[data-id="+tile_id+"]").find(".tileDescription").text();
  DEBUG.logDebug("Parent Tile Name :" + tile_name);  
  $("#tile_name").val(tile_name);

  $("#tile-mqtt-path").val("home/" + tile_id);

  $(".modal-edit-item-delete").on("click",function(e){
    // ( > modal_edit_events.js )
    modalEditItemDelete(this);
  });

  $(".modal_edit_item_textbox").on("input",function(e){
    // ( > modal_edit_events.js )
    modalEditItemTextChanged(this);
  });

  $(".modal_edit_tile_textbox").on("input",function(e){
    // ( > modal_edit_events.js )
    modalEditTileTextChanged(this);
  });
  
  $("#tile-id").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileIDchanged(this);
  });

  
  $(".modal_edit_type_text").each(function() {
    var type_name = $(this).text();
    var id_of_caller = $(".modal-here").attr("id_of_caller");
    
    Hammer(this).on("tap", function() {
      // ( > modal_edit_events.js )
      tileTypeChanged(id_of_caller,type_name);
    });
  });
  
  $("#tile_name").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileTitleChanged();
  });
  initImages();

}