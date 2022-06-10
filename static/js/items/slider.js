"use strict";

class itemSlider {
  constructor() {
    this.type = "slider";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {
    let key;

    if (config.range === true) {
      key = "values"
      $(self).find(".modal-slider-value").text(value[0] + " - " + value[1]);
    }
    else {
      key = "value"
      $(self).find("label").text(config.label);
      $(self).find(".modal-slider-value").text(value);
    }

    $(self).find(".slider").slider(key, value);
  }

  valueTransmit(object) {
    let initConfig = store(object, "config");
    let initValue = store(object, "value");
    object.find('.slider').slider({
        slide: function(event, ui) {
          let config = store(object, "config");
          let value;
          if (config.range === true) {
            value = $(this).slider("values")
            value[ui.handleIndex] = ui.value
            object.find(".modal-slider-value").text(value[0] + " - " + value[1]);
          }
          else {
            value = ui.value;
            object.find(".modal-slider-value").text(value);
          }

          if (config["smooth"] === true) {
            object.find(".modal-slider-right").css("opacity", 1);
            store(object, "value", value).trigger("value-transmit");
          }
          else {
            object.find(".modal-slider-right").css("opacity", 0.6);
          }
        },
        stop: function(event, ui) {
          let config = store(object, "config");

          if (!(config["smooth"])) {
            // Send only if slider changed value
            object.find(".modal-slider-right").css("opacity", 1);
            let value;
            if (config.range === true) {
              value = $(this).slider("values");
              object.find(".modal-slider-value").text(value[0] + " - " + value[1]);
            }
            else {
              value = ui.value;
              object.find(".modal-slider-value").text(value);
            }
            store(object, "value", value).trigger("value-transmit");
          }
        },
        animate: "fast",
        min: initConfig.min,
        max: initConfig.max,
        value:  initConfig.range ? null : (Array.isArray(initValue) ? initValue[0] : initValue),
        values: initConfig.range ? (Array.isArray(initValue) ? initValue    : [initValue, initValue]) : null,
        range: initConfig.range ? true : "min",
        step: initConfig.step,
        disabled: initConfig.disabled
    });
  }

  configReceive(object, self, value, config) {
    let range = config.range;
    if (range !== true) range = "min";

    $(self).find(".modal-slider-label").text(config.label);
    $(self).find(".modal-slider-suffix").text(" " + config.suffix);
    let options = {
      range: range,
      min: config["min"],
      max: config["max"],
      step: config["step"],
      disabled: config["disabled"]};

    $(self).find(".slider").slider("option", options);

    if (range === true) {
      if (!(Array.isArray(value))) {
        let sliderValue = $(self).find(".slider").slider("values");
        if(!(sliderValue) || (sliderValue[0] === 0 && sliderValue[1] === 0)) {
          $(self).find(".slider").slider("option", "values", [value, value]);
        }
      }
      else {
        $(self).find(".slider").slider("option", "values", value);
      }
    }
    else {
      if (Array.isArray(value)) {
        if(!($(self).find(".slider").slider("value"))) {
          $(self).find(".slider").slider("option", "value", value[0]);
        }
      }
    }
  }
}