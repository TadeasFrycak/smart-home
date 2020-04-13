$(document).ready(function(){
  init_tile_modal();
});


function sliders_init(value){
  var tile_id = $("#tile-id").val();
  $("#tile-mqtt-path").val("home/" + tile_id);

  sliders = [];

  $(".time-picker-pickie").each(function(test) {
    $(this).timepicki({show_meridian:false, max_hour_value:23});
    $(this).attr("readonly", "readonly");
    $(".timepicki-input").attr("readonly", "readonly");
  });

  $(".modal-edit-item-delete").on("click",function(e){
    var id_of_caller = $(".modal-here").attr("id_of_caller");

    var textbox_wrapper = $(this);
    var wrapper_index = 0
    $(".modal_items_edit_sortable_item").each(function(e){
      if ($(this).has(textbox_wrapper).length == 1) return false;
        wrapper_index += 1;
    })
    
    $.post( "/modal_item_delete", {
      "tile_id": id_of_caller,
      "index" : wrapper_index
    });

    $(this).parent().parent().parent().slideUp();
    setTimeout(() => {$(this).parent().parent().parent().remove();}, 600);


  });

  $(".modal_edit_item_textbox").on("input",function(e){

    var module_id = $(this).val();
    if (module_id.length <= 5) { $(this).addClass("is-invalid"); }
    else { $(this).removeClass("is-invalid"); }

    var id_of_caller = $(".modal-here").attr("id_of_caller");
    var textbox_old_val = $(this).attr("placeholder");
    var textbox_new_val = $(this).val();

    var textbox_wrapper = $(this);
    var wrapper_index = 0
    $(".modal_items_edit_sortable_item").each(function(e){
      if ($(this).has(textbox_wrapper).length == 1)
      {
        return false;
      }
        wrapper_index += 1;
    })

    $.post("/modal_item_value_rwr", {
      "tile_id": id_of_caller,
      "old_value": textbox_old_val,
      "new_value": textbox_new_val,
      "index" : wrapper_index
    });

    var textbox_old_val = $(this).attr("placeholder",textbox_new_val);

  });


  $("#tile-id").on("input",function(e){
    var tile_id = $(this).val();

    if (tile_id.length <= 5) { $(this).addClass("is-invalid"); }
    else { $(this).removeClass("is-invalid"); }

    var id_of_caller = $(".modal-here").attr("id_of_caller");
    $("#tile-mqtt-path").val("home/" + tile_id);
    $.post( "/tile_id_rwr", {
      "tile_id": id_of_caller,
      "new_id": tile_id
    });

    $(".modal-here").attr("id_of_caller", tile_id);
  });

  $("#tile_name").on("input",function(e){
    var tile_name = $("#tile_name").val();
    var tile_id = $("#tile-id").val();
    var id_of_caller = $(".modal-here").attr("id_of_caller");
    $("#tile-mqtt-path").val("home/" + tile_id);
    $.post( "/tile_name_rwr", {
      "tile_id": id_of_caller,
      "new_name": tile_name
    });
  });

  // // FS: TODO double sending
  // $(".modal_edit_tile_type").on("click",function(e){
  //   console.log("tap.");
  //   var type_name = $(this).find(".modal_edit_type_text").text();
  //   console.log("Type name1: " + type_name);
  // });

  $(".modal_edit_type_text").each(function() {
    var type_name = $(this).text();
    var id_of_caller = $(".modal-here").attr("id_of_caller");
    Hammer(this).on("tap", function() {
      console.log("Click!");
      $.post( "/tile_type_rwr", {
          "id": id_of_caller,
          "new_type": type_name
        }, function(response){
          var json = JSON.parse(response);
          console.log(json);
          $(".tile-type-wrapper").empty();
          $(".tile-type-wrapper").append(json.tile_values);

          initImages();

        });

      
    });
  });

  initImages();


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
}

function tileGetAtributeByName(obj, desc){
  return obj.find("." + desc).text();
}

function init_tile_modal()
{
  $(".tileModal").each(function(){
    var $this = $(this);
    var hammer = new Hammer(this);
    initTilePress(hammer, $this,0);
    
  });
}


function initTilePress(hammer, $this, add_new_item)
{
  hammer.on("press", function() {
    console.log("press");
    var object_id = $this.parent().attr("data-id");
    

    var to_send;
    if (editMode === false) to_send = 0;
    else if (editMode === true) to_send = 1;

    $.post("/get_modal", {
      "id": object_id,
      "edit": to_send,
      "add": add_new_item,
      "page_index": swiper.realIndex
    }, function(result){
      var json = JSON.parse(result);
      $(".modal-here").empty();
      $(".modal-here").append(json.modal);

      $("#myModal").modal({ keyboard: true })

      $('#myModal').on('hidden.bs.modal', function () {
        if (editMode == true){
          var tile_id = $(".modal-here").attr("id_of_caller");

          tile_id = $("#tile-id").val();
          console.log("Tile ID: "+ tile_id);

          $.post( "/get_tile", {
            "tile_id": tile_id
          }, 
          function(result){
            var json = JSON.parse(result);
            var newID = json.id;

            var tileS = $(".tile[data-id='"+tile_id+"']");

            var found = 0;
            $(".tile").each(function() {
              var search_id = $(this).attr("data-id");
              if (search_id == newID) {found = 1;}
              // console.log("Data-ID: " + search_id);
            });
            if (found > 1) {console.log("! Warning ! more than one ID found! (modal_init.js; ln: 183)")};
            if (found == 0) {
              $(json.tile).insertBefore(".swiper-slide-active .tile_ghost_prefab_class").hide().fadeIn();
            }
            else {
              if (json.tile !== "") {
                $(tileS).parent().replaceWith(json.tile);
              }
              else {
                $(tileS).parent().show().fadeOut();
                setTimeout(() => {$(tileS).parent().remove();}, 1000);
              }
            }

            var hammerTime = $(".tile[data-id='"+newID+"']").find(".tileModal")[0];
            var $hammerTime = $(hammerTime);
            var newHammer = new Hammer(hammerTime);
            initTilePress(newHammer,$hammerTime,0);
            tileToggleTap(hammerTime);

            var $tileStat = $(tileS).find(".tileStatus")[0];
            var tile_pre = $(".tile[data-id='"+newID+"']");

              if ($($tileStat).text() === "ON"){
                $(tile_pre).toggleClass("tileActive");
                $(tile_pre).find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
              }

          });
          
        }
      })
      var header = tileGetAtributeByName($this.parent(),"tileDescription");
      $(".modal-title").text(header);
      $(".modal-here").attr("id_of_caller", object_id);
      console.log(object_id);
      if (object_id === undefined) {
        tile_id = $("#tile-id").val();
        console.log(tile_id);
        $(".modal-here").attr("id_of_caller", tile_id);
      }

      sliders_init(object_id);

      $(".modal_items_edit_sortable_item_dropdown").slideUp();

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
                  gradientToColors: [ "#FDD835"],
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

      $(".modal_toggle").each(function(){
        var x = $(this).parent().parent().parent().attr("data-id");
        for (j in json.toggles) {
          if (x === j) {
            $(this).prop("checked", parseInt(json.toggles[j]));
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
}

function initImages(){
  $(".modal-edit-select-img").each(function() {
    var attr = $(this).attr('checked');
    if (typeof attr !== typeof undefined && attr !== false) {
      $(this).css({"border": "2px solid rgb(23, 162, 184)"});
    }
    Hammer(this).on("tap", function(elem) {
      $(".modal-edit-select-img").each(function() {
        $(this).css({"border": "2px solid transparent"});
      });
      $(elem.target).css({"border": "2px solid rgb(23, 162, 184)"});
      var name = $(elem.target).attr("-data-name");
      var tile_id = $(".modal-here").attr("id_of_caller");
      $.post( "/tile_icon_rwr", {
        "id": tile_id,
        "new_icon": name
      }, function(result){});
    });
  });
}