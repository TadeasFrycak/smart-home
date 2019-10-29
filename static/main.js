$(document).ready(function(){ 
  
  console.log("+----------------------------------+");
  console.log("|     IoT Project, version 10.4    |");
  console.log("|     Last modified: 27.10.2019    |");
  console.log("|                                  |");
  console.log("|              © 2019              |");
  console.log("+----------------------------------+");

  var slider_prew_val = 0;

  var sliders = [];
  // Asynchroní přijem dat
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/acom");
    socket.on("tile", function(msg) {
      // console.log($(document).find(msg.i).html());
      $(".tile").each(function() {
        var atributeOfCurrentItem = $(this).attr("data-id");
        if (atributeOfCurrentItem == msg.i)
        { 
          var typeOfItem = $(this).attr("data-type");

          if (typeOfItem == "toggle"){

            var prewTileState = $(this).find(".tileStatus").text();
            var curTileState = msg.v;

            if (prewTileState == "ON" && curTileState == 0)     { $(this).find(".tileStatus").text("OFF"); $(this).toggleClass('tileActive'); }
            else if (prewTileState== "OFF" && curTileState > 0) { $(this).find(".tileStatus").text("ON"); $(this).toggleClass('tileActive'); } 
          
          } 
          else if (typeOfItem == "percentage")
          {
            $(this).find(".tileInputVal").text(msg.v);
          }

        }
      });
    });

    socket.on("slider", function(msg) {
      for (i=0; i< sliders.length; i++) {
        var slider_html = sliders[i].selector.offsetParent.outerHTML;
        var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");
        if (slider_detect_id == msg.i){
          sliders[i].value(msg.v);
        }
      };
    });

  $(".tileStatus").each(function() {
    //console.log($(this).parent().parent().attr("data-id"));
    if ($(this).text() == "ON"){
      $(this).parent().parent().toggleClass('tileActive');
    }
  });



  /**
   * 
   *  Globální promněné
   * 
   */
    
   // Definování CSS barev do proměnných
  var item_unactive_color = 'rgb(206, 206, 206)';
  var item_active_color = 'rgb(255, 10, 255)';
  


  /**
   * 
   *  Kód pro initializování objektů
   * 
   */
  
/*
  $('.slider').each(function(){
    slider = new hx.Slider(this,{max:100});
  });

  $(".slider").each(function() {
    slider = new hx.Slider(this);
    slider.change(function(value) {
        console.log("test");
    });
*/    

function initModules(value){
  $(".slider").each(function(test) {
    slider = new hx.Slider(this, {max:100});
    sliders[test] = slider;
    slider.on('change', function(data){
        //console.log(data.html.getAttribute("data-id"));
        //console.log(data.html);

        var string = data.html;
        var slider_id = $($.parseHTML(string)).attr("data-id");
        var slider_value = Math.round(data.value);
        //console.log(jqueryObject.attr("data-id"));
        if (slider_prew_val != slider_value)
        {
          slider_prew_val = slider_value;  
          $.post( "/slider", {
                  "i": slider_id,
                  "v": slider_value,
                  "id_tile": value
          },
          function(result){
                  // console.log(result);
          });
        }

    });
    $(slider).each(function() {
      var slider_html = slider.selector.offsetParent.outerHTML;
      var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");
      $.post("/slider_setting", {
        "i": slider_detect_id,
        "id_tile": value
      },
      function(result){
        $(slider).each(function() {
          /*var slider_html = slider.selector.offsetParent.outerHTML;
          var slider_detect_id = $($.parseHTML(slider_html)).attr("data-id");
          console.log("Found " + slider_detect_id + ", searching for: ");
          if (slider_detect_id == JSON.parse(result).i){
            slider.value(JSON.parse(result).v);
            console.log(JSON.parse(result).v);
          }*/
        });


        console.log(result);
        //slider.value(JSON.parse(result).v);
        
      });
    });
    

  });

  $('select').formSelect();
  $('.timepicker').timepicker();

  $('.graphModul').each(function(){
    var chartXaxis = ['1.1.2019','1.2.2019','1.3.2019','1.4.2019', '1.5.2109'];
    var chartData = [12,10,-1,9,1]
    var header = this.getAttribute("data-header");
  
    //var ctx = document.getElementById('myChart');
    var ctx = $(this).children();
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartXaxis,
            datasets: [{
                label: header,
                data: chartData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
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




/**
 * 
 *  Kód pro zpracovávání inputů ze stránky
 * 
 */



  
  // CheckBox; 
  //$('input[type="checkbox"]').click(function(){
  //$('.toggle-slider').click(function(){
  $('.input[type="checkbox"]').on('click', function(e) {
    var IDofObject = $(this).parent().parent().parent().attr("data-id");
    console.log("aaa");

    if($(this).prop("checked") == true){
      var stateOfObject = "checked";
      printToConsole(IDofObject, stateOfObject);
    }
    else if($(this).prop("checked") == false){
      var stateOfObject = "unchecked";
      printToConsole(IDofObject, stateOfObject);
    }
  });


  $('.tileToggle').each(function(){
      var $this = $(this);
      var mc = new Hammer(this); 
      mc.on("tap", function() {

          $this.parent().toggleClass('tileActive');
          
          var tile_id = $this.parent().attr("data-id");
          var tile_state = 0;

          var tile_state = $this.parent().find(".tileStatus").text();
          if (tile_state == "ON") { $this.parent().find(".tileStatus").text("OFF"); tile_state = 0; }
          else if (tile_state == "OFF") { $this.parent().find(".tileStatus").text("ON"); tile_state = 1; }

          $.post("/tile", {
              "i": tile_id,
              "v": tile_state
          },
              function(result){
          });
      });
  });

  $('.tileModal').each(function(){
    var $this = $(this);
    var mc = new Hammer(this);
    mc.on("press", function() {
      // console.log($this.parent().attr("data-id"));
      var IDofObject = $this.parent().attr("data-id");
      //console.log(IDofObject);
      var value = IDofObject

      $.post( "/get_modal", {
            "type": "modal",
            "i": value
        },
        
        function(result){
          //console.log(result);
          //console.log(data);
          $(".modalHere").append(result);
          genModal().style.display = "block";
          initModules(value);
          var header = tileGetAtributeByName($this.parent(),"tileDescription");
          $(".modalHeader").text(header);
      });

      


    });
  });
  
  function printToConsole(objID, state){
    console.log(objID + " is " + state);
  }

  function tileGetAtributeByName(obj, desc){
    return obj.find("." + desc).text();
  }



  /**
   * 
   *  Genreování modalového okna
   * 
   */  
  function genModal(){
      var modal = document.getElementById("tile-Modal");
      var span = document.getElementsByClassName("close")[0];

      span.onclick = function() {
      modal.style.display = "none";
      $(".modalHere").empty();
      }
      // Close the modal when close button is pressed
      window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        $(".modalHere").empty();
      }
    }
    return modal;
  }



 
  // Initializace Swiperu 
  var swiper = new Swiper('.swiper-container', {
    pagination: { el: '.swiper-pagination'},
    threshold: '10',
    //allowTouchMove: false,
    //simulateTouch: false,
    //touchStartPreventDefault: true,
    //noSwiping: true,
    //noSwipingClass = 'swiper-no-swiping'
  });  


  function changeTile(){
    var s_ON = false;
    var s_VAL = 0;
  }
 

});