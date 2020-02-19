$(document).ready(function() {
  console.log("+----------------------------------+");
  console.log("|     IoT Project, version 10.6    |");
  console.log("|     Last modified: 30.10.2019    |");
  console.log("|                                  |");
  console.log("|          ©  2019 - 2020          |");
  console.log("+----------------------------------+");

  // ----------------------------------------------
  // Define some constants variables
  // ----------------------------------------------


is_edit = false;


  var slider_previous_value = 0;
  sliders = [];
  var graphs = [];
  var graphs_id = [];
    device_number = Math.round(Math.random() * 1000);

    var item_unactive_color = "rgb(206, 206, 206)";
    var item_active_color = "rgb(255, 10, 255)";

    var GaugesByID = [];

    // ----------------------------------------------
    // Initialization of objects
    // ----------------------------------------------

    
    $(function () {

        var gaugeOptions = {
    
            chart: {
                    type: 'solidgauge',
                        margin: [0, 0, 0, 0],
                        backgroundColor: 'transparent'
                    },
                    title: null,
                    yAxis: {
                        min: 0,
                        max: 30,
                        minColor: '#009CE8',
                        maxColor: '#009CE8',
                        lineWidth: 0,
                        tickWidth: 0,
                        minorTickLength: 0,
                        minTickInterval: 500,
                        labels: {
                            enabled: false
                        }
                    },
                    pane: {
                        size: '100%',
                        center: ['50%', '60%'],
                        startAngle: -130,
                        endAngle: 130,
                        background: {
                        borderWidth: 20,
                        backgroundColor: '#DBDBDB',
                        shape: 'arc',
                        borderColor: '#DBDBDB',
                            outerRadius: '90%',
                            innerRadius: '90%'
                        }
                    },
                    tooltip: {
                        enabled: false
                    },
                    plotOptions: {
                        solidgauge: {
                            borderColor: '#009CE8',
                            borderWidth: 20,
                            radius: 90,
                            innerRadius: '90%',
                            dataLabels: {
                                y: 5,
                                borderWidth: 0,
                                useHTML: true
                            }
                        }
                    },
                    series: [{
                        name: 'windSpeed',
                        data: [5],
                        dataLabels: {
                            format: '<div style="Width: 50px;text-align:center"><span style="font-size:30px;color:#009ce8">{y}</span></div>'
                        }
                        
                    }],
    
                credits: {
                    enabled: false
                },
        };
    
        // The speed gauge
        $('#container-speed').highcharts(gaugeOptions);
        
        // Tweak SVG
        var svg;
        svg = document.getElementsByTagName('svg');
        if (svg.length > 0) {
            var path = svg[0].getElementsByTagName('path');
            if (path.length > 1) {
                // First path is gauge background
                path[0].setAttributeNS(null, 'stroke-linejoin', 'round');
                // Second path is gauge value
                path[1].setAttributeNS(null, 'stroke-linejoin', 'round');
            }
        }
        
        // Bring life to the dials
        setInterval(function () {
            // Speed
            var chart = $('#container-speed').highcharts(),
                point,
                newVal;
    
            if (chart) {
                point = chart.series[0].points[0];
                newVal = Math.round(Math.random() * 25+2);
                point.update(newVal);
            }
    
        }, 5000);
    
    
    });

    
    
    // });

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
});



