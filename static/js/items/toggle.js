"use strict";

class itemToggle {
  constructor() {
    this.type = "toggle";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {
    let binaryValue;

    if (value === config["on_state"]) {
      binaryValue = 1;
    }

    else if (value === config["off_state"]){
      binaryValue = 0;
    }

    else {
      return null;
    }

    $(self).find(".switch").prop("checked", binaryValue);
  }

  valueTransmit(object) {
    object.on("change", ".switch", function() {
      let config = store(object, "config");
      let value = $(this).prop("checked");

      if (value) {
        value = config["on_value"]
      }
      else {
        value = config["off_value"]
      }
      store(object, "value", value).trigger("value-transmit");
    });
  }

  configReceive(object, self, value, config) {
    $(self).find(".switch").prop("disabled", config.disabled ? 1 : 0);
    $(self).find(".modal-toggle-label").text(config.label);
    $(self).find(".modal-toggle-input").find("label").text(config.placeholder);
  }
}