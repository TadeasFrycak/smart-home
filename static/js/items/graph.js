"use strict";

class itemGraph {
  // TODO zprovoznit společně s algoritmem
  constructor() {
    this.type = "graph";
  }

  setup(object) {
    let value = store(object, "value");
    console.log(value);
    console.log(typeof value)
    value["x"].forEach(function(val, index) {
      value["x"][index] = new Date(val*1000);
    });

    let config = {
      type: 'line',
      data: {
        labels: value.x,
        datasets: [{
          label: store(object, "config")["label"],
          // backgroundColor: utils.transparentize(presets.red),
          borderColor: "rgb(255, 99, 132)",
          data: value.y,
          fill: "start",
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: store(object, "config")["label"]
        },
        legend: {
          display: false
        },
        tooltips: {
          mode: 'index',
          intersect: false,
        },
        hover: {
          mode: 'nearest',
          intersect: true
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                  quarter: "MMM YYYY"
              }
            },
            display: true,
            scaleLabel: {
                display: false,
                labelString: 'Month'
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              display: false,
              labelString: 'Value'
            }
          }]
        }
      }
    };

    store($(object).find("canvas"), "graph-config", config);

    let ctx = document.getElementById('canvas').getContext('2d');
    let graph = new Chart(ctx, config);
    store($(object).find("canvas"), "graph", graph);
    // TODO remove in 0.11.9
    /*object.each(function(){
      let value = store(this, "value");
      new Chart($(this).children(), {
        type: "line",
        data: {
          labels: value.x,
          datasets: [{
            label: store(this, "header"),
            borderColor: "rgb(255, 99, 132)",
            data: value.y
          }]
        },
        options: {
          scales: {
            xAxes: [{
              type: 'time',
            }],
          yAxes: [{
            ticks: {
              // beginAtZero: true
            }
          }]
        }}
      });
    });*/
  }

  valueReceive(object, self, value, config) {
    console.log("new", value);
    let graphConfig = store($(object).find("canvas"), "graph-config");
    graphConfig.data.labels.push(new Date(value.x * 1000));

    graphConfig.data.datasets.forEach(function(dataset) {
      dataset.data.push(value.y);
    });
    store($(object).find("canvas"), "graph").update();
  }

  valueTransmit(object) {}

  configReceive(object, self, value, config) {}
}