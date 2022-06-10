"use strict";
// TODO mousedown a mouseup - bude fungovat i podržení

class itemButton {
  constructor() {
    this.type = "button";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {}

  valueTransmit(object) {
    object.on("click", "button", function() {
      let config = store(object, "config");

      store(object, "value", config["on_value"]).trigger("value-transmit");
    });
  }

  configReceive(object, self, value, config) {
    $(self).find("button").text(config.label);
    $(self).find("button").removeClass(function (index, className) {
      return (className.match (/(^|\s)btn-\S+/g) || []).join(' ');
    });

    $(self).find("button").addClass("btn-" + config.color);
  }
}