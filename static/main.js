$(document).ready(function(){     

  $('.slider').each(function(){
    slider = new hx.Slider(this,{max:100});
  });
  $('.toggle').each(function(){
    var toggle = new hx.Toggle(this)
  });

  slider.on('change', function(){
    console.log("aa");
  });

  $('.timepicker').timepicker();
  

    // Definování CSS barev do proměnných
    var item_unactive_color = 'rgb(206, 206, 206)';
    var item_active_color = 'rgb(255, 10, 255)';


    // Get the modal
    var modal = document.getElementById("tile-Modal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
    modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

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
          modal.style.display = "block";
          var header = tileGetAtributeByName($this.parent(),"tileDescription");
          $(".modalHeader").text(header);
      });
  });

  function tileGetAtributeByName(obj, desc){
    return obj.find("." + desc).text();
  }



  $('.graphModul').each(function(){
    var chartXaxis = ['1.1.2019','1.2.2019','1.3.2019','1.4.2019', ];
    var chartData = [12,10,-1,9]
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






  $('.hx.Slider').on('change', function(e){
    console.log("aslkdmsjdn");
  });








 

});