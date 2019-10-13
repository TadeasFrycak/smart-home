$(document).ready(function(){ 
  
  console.log("+----------------------------------+");
  console.log("|     IoT Project, version 12.2     |");
  console.log("|     Last modified: 13.10.2019     |");
  console.log("|                                  |");
  console.log("|              © 2019              |");
  console.log("+----------------------------------+");


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

function initModules(){
  $(".slider").each(function() {
    slider = new hx.Slider(this, {max:100});

    slider.on('change', function(value){
      // var target = $( slider.target );
      value = Math.round(value);
      //   console.log(target.parent().parent().parent().html());
      //   console.log(x);
        $.post( "/io", {
                data: value
            },
        function(result){
                console.log(result);
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
  $('input[type="checkbox"]').click(function(){
    var IDofObject = $(this).parent().parent().parent().attr("data-id");

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
      });
  });

  $('.tileModal').each(function(){
    var $this = $(this);
    var mc = new Hammer(this);
    mc.on("press", function() {
      var IDofObject = $this.parent().attr("data-id");
      //console.log(IDofObject);
      var value = IDofObject

      $.post( "/get_modal", {
            type: "modal",
            id: value
        },
        
        function(result){
          //console.log(result);
          //console.log(data);
          $(".modalHere").append(result);
          genModal().style.display = "block";
          initModules();
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