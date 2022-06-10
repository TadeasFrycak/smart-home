"use strict";

class itemProgressBar {
  constructor() {
    this.type = "progress_bar";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {
    $(self).find(".progress-bar").attr("aria-valuenow", value);
    $(self).find(".progress-bar").css("width", value * (100 / (config.max + config.min)) + "%");
  }

  valueTransmit(object) {}

  configReceive(object, self, value, config) {
    $(self).find(".progress-bar").attr("aria-valuemax", config.max);
    $(self).find(".progress-bar").attr("aria-valuemin", config.min);

    $(self).find(".progress-bar").attr("aria-valuenow", value);
    $(self).find(".progress-bar").css("width", (value - parseFloat(config.min)) * (100 / (parseFloat(config.max) - parseFloat(config.min))) + "%");

    $(self).find(".progress-bar").text(config.label);
    $(self).find(".progress-bar").removeClass(function (index, className) {
      return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
    });
    $(self).find(".progress-bar").addClass("bg-" + config.color)
  }
}