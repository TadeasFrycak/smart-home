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
    // RequestModal($this, add_new_item);
    let isEditActive = $("body").attr("data-is-edit-active");
    if (isEditActive === "false")
    {
      RequestModal($this, add_new_item);
    }
  });
}

function initTileTap(hammer, $this, add_new_item)
{
  hammer.on("tap", function() {
    // ( > modal_init.js )
    // terminal.log("Tapped!");
    let isEditActive = $("body").attr("data-is-edit-active");
    if (isEditActive == "true")
    {
      RequestModal($this, add_new_item);
      console.log("Requested modal!");
    }
    else if ($($this).attr("data-type") == "toggle"){
      tappedOnToggle($this)
    }

  });
}

function initImages(){
  $(".modal-edit-icon").each(function() {

    // let attr = $(this).attr('checked'); 

    // if (typeof attr !== typeof undefined && attr !== false) {
    if ($(this).attr('data-selected') == "true"){
      if ($("body").hasClass("dark")) {
        $(this).css({"border": "2px solid rgb(232, 93, 71)"});
      }
      else {
        $(this).css({"border": "2px solid rgb(23, 162, 184)"});
      }
    }
    Hammer(this).on("tap", function(elem) {
      // ( > modal_edit_events.js )
      modalEditPreviewImageTap(elem);
    });
  });
}


// /get_modal 
//    > tileId

// /get_add_tile_modal
//    > slideIndex

// /get_edit_modal
//    > tileId

// function addNewTile()
// {
//   socketio.emit("get_add_modal", {"slide_index": swiper.realIndex});
// }

function requestNormalModal($this)
{
  let object_id = $this.parent().attr("data-id");
  socketio.emit("get_modal", {"tile_id": object_id, "tab_id": sessionStorage.tabID});
}

function requestEditModal($this)
{
  let object_id = $this.parent().attr("data-id");

  if ($this.parent().attr("data-type") == "add-new-tile")
  {
    socketio.emit("get_add_modal", {"slide_index": swiper.realIndex, "tab_id": sessionStorage.tabID});
  }
  else {
    socketio.emit("get_edit_modal", {"tile_id": object_id, "tab_id": sessionStorage.tabID});
  }
  
}

function handleModalResponse(data)
{
  // ( > modal_init.js )
  initializeModal(data);
}

function initializeModal(data)
{
    let object_id = data.tile_id;

    $(".modal-here").empty();
    $(".modal-here").append(data.modal);
    $("#myModal").modal({ keyboard: true });
    $("#myModal").on("hide.bs.modal", function (e) {
      modalClose();
    });
    // var header = tileGetAtributeByName($this.parent(),"tile-label");
    // $(".modal-title").text(header);
    $(".modal-here").attr("id_of_caller", object_id);

    if (object_id === undefined) {
      tile_id = $("#tile-id").val();
      $(".modal-here").attr("id_of_caller", tile_id);
    }

    $(".modal-edit-item-dropdown").slideUp();
    // ( > modal_init.js )
    initializeAllItemsWithinModal(data);
}

// function updateMySlider(id, value)
// {
//     // update position
//     const triggerEvents = true; // or false
//     var yy = document.querySelector(".slider[data-id="+id+"] input[type='range']")

//     yy.rangeSlider.update({
//         min : 0,
//         max : 20, 
//         step : 0.5,
//         value : value
//     }, triggerEvents);
// }

function initializeAllItemsWithinModal(data)
{
  /*
  *   V normálním režimu   
  */

  // terminal.log(data);
  // terminal.log(value);

  
  $(".slider").each(function(){

    var slider = $(this).find('input[type="range"]');
    rangeSlider.create(slider, {
      onSlide: function (position, value) {

      slider_div = $(this.range).parent();  
      slider_prew_value = slider_div.attr("data-prew-val");

      // Send only if slider changed value
      if (position != slider_prew_value)
      {
        slider_div.attr("data-prew-val", position);
        slider_id = slider_div.attr("data-id");
        // terminal.log(slider_id);
        // terminal.log('onSlide', 'position: ' + position, 'value: ' + value);
  
        let id_of_caller = $(".modal-here").attr("id_of_caller");
  
        socketio.emit("modal_slider", {
          "value": position,
          "id": slider_id,
          "tile_id": id_of_caller
        });
      }
    }
    });
  });

  let currentDate = new Date();
  let datetime = currentDate.getHours() + ":" + currentDate.getMinutes()

  $(".clockpicker").clockpicker({
    default: datetime,
    placement: "auto",
    donetext: _("Done"),
  });

  $("input.clockpicker").change(function(e) {
      let tileID = $(".modal-here").attr("id_of_caller");
      let itemID = $(this).attr("data-id");
      socketio.emit("modal_clockpicker", {"tile_id": tileID, "item_id": itemID, "value": $(this).val()});
  });

  $(".modal-daterangepicker-input").each(function(){

    let rangePickerId = $(this).attr("id");

    let start = moment().subtract(29, 'days');
    let end = moment();

    function cb(start, end) {
      $(".modal-daterangepicker-input[id="+rangePickerId+"]").find("span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
      let id_of_caller = $(".modal-here").attr("id_of_caller");
      let pair_id = $(".modal-daterangepicker-input[id="+rangePickerId+"]").parent().attr("data-pair");

      socketio.emit("modal_daterangepicker", {
        "pair_id" : pair_id,
        "tile_id" : id_of_caller,
        "id": rangePickerId,
        "start_value": moment(start).format("YYYY-MM-DD hh:mm:ss"),
        "end_value": moment(end).format("YYYY-MM-DD hh:mm:ss")
      });
    }

    $(".modal-daterangepicker-input[id="+rangePickerId+"]").daterangepicker({
        // timePicker: true,
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 1901,
        maxYear: parseInt(moment().format('YYYY'),10)
        // startDate: start,
        // singleDatePicker: true,
        // showDropdowns: true,
        // endDate: end,
        // ranges: {
        //    "Today": [moment(), moment()],
        //    "Yesterday": [moment().subtract(1, "days"), moment().subtract(1, "days")],
        //    "Last 7 Days": [moment().subtract(6, "days"), moment()],
        //    "Last 30 Days": [moment().subtract(29, "days"), moment()]
        //   //  "This Month": [moment().startOf("month"), moment().endOf("month")],
        //   //  "Last Month": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
        // },
        // locale: {
        //   format: "M/DD hh:mm A"
        // }
    }, cb);

    // cb(start, end);

    for (var k in data.daterangepickers){
      if (k == rangePickerId){ 
        let dateStart = moment(data.daterangepickers[k].start).format("MMMM D, YYYY");
        let dateEnd = moment(data.daterangepickers[k].end).format("MMMM D, YYYY");
        $(".modal-daterangepicker-input[id="+rangePickerId+"]").find("span").html(dateStart + " - " + dateEnd);
      }
    }
      
    

  });

  $(".modal-graph").each(function(){
    for (k in data.graphs){
      if (k == $(this).attr("data-id")){ // Nasel graf sse setejným ID
        let ctx = $(this).children();
        let new_chart = new Chart(ctx, {
          type: "line",
          data: {
            labels: data.graphs[k].data_x,
            datasets: [{
                label: $(this).attr("data-header"),
                borderColor: "rgb(255, 99, 132)",
                data: data.graphs[k].data_y
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
    for (k in data.graphs){
        if (k == $(this).attr("data-id")) {  // Nasel graf sse setejným ID
        var myData = data.graphs[k].values;
        var graph_name = data.graphs[k].label;
        var x_min = data.graphs[k].max_min.x.min;
        var x_max = data.graphs[k].max_min.x.max;
        var y_min = data.graphs[k].max_min.y.min;
        var y_max = data.graphs[k].max_min.y.max;

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
                            
        let chart = new ApexCharts(document.querySelector("#"+k), options);
        chart.render();
                            
        let optionsLine = {
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

        let chartLine = new ApexCharts(document.querySelector("#"+k+"_brush"), optionsLine);
        chartLine.render();
        }
    }
  });

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
  var tile_name = $(".tile[data-id="+tile_id+"]").find(".tile-label").text();
  DEBUG.logDebug("Parent Tile Name :" + tile_name);  
  $("#tile_name").val(tile_name);

  $("#tile-mqtt-path").val("home/" + tile_id);

  $(".modal-edit-item-delete").on("click",function(e){
    // ( > modal_edit_events.js )
    modalEditItemDelete(this);
  });

  $(".modal-edit-item-dynamic-value").on("input",function(e){
    // ( > modal_edit_events.js )
    modalEditItemTextChanged(this);
  });

  $(".modal-edit-tile-dynamic-value").on("input",function(e){
    // ( > modal_edit_events.js )
    modalEditTileTextChanged(this);
  });
  
  $("#tile-id").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileIDchanged(this);
  });

  $(".modal-edit-tile-type").on("click",  function() {
    // terminal.log("Tile typed changed");
    // TODO double bug
    // ( > modal_edit_events.js )
    let type_name = $(this).text();
    let id_of_caller = $(".modal-here").attr("id_of_caller");

    tileTypeChanged(id_of_caller,type_name);
  });
  
  $("#tile_name").on("input",function(){
    // ( > modal_edit_events.js )
    modalEditTileTitleChanged();
  });

  initImages();

  // Unfocus input 
  $(".unfocus-on-enter").keydown(function(event){
    event.keyCode===13 && $(this).blur();
  });
}