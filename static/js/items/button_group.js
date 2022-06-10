"use strict";

class itemButtonGroup {
  constructor() {
    this.type = "button_group";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {
    if (config.checkbox) {
      object.find("input").parent().removeClass("active");
      value.forEach(function(val, index) {
        object.find("input[data-name='" + val +"'").parent().addClass("active");
      });
    }
    else {
      object.find("input").parent().removeClass("active");
      object.find("input[data-name='" + value +"']").parent().addClass("active");
    }
  }

  valueTransmit(object) {
    object.find("label").on("click", "input",  function() {
      let config = store(object, "config");
      let value;

      if (!config.checkbox) {
        object.find("input").parent().removeClass("active");
      }
      $(this).parent().toggleClass("active");

      if (config.checkbox) {
        value = [];
        object.find("input").each(function() {
          if ($(this).parent().hasClass("active")) {
            value.push(store(this, "name"));
          }
        });
      }
      else {
        value = store(this, "name");
      }
      store(object, "value", value).trigger("value-transmit");
    });
  }

  configReceive(object, self, value, config) {
    $(self).find(".col-form-label").text(config.label);
  }
}