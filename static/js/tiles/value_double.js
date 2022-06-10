"use strict";

class tileValueDouble {
  constructor() {
    this.type = "value_double";
  }

  setup(object) {}

  tap(object, self, config) {}

  valueReceive(object, self, value, config) {
    $(self).find(".tile-value-left").text(value.left.value);
    $(self).find(".tile-value-right").text(value.right.value);
    $(self).find(".tile-suffix-left").text(value.left.suffix);
    $(self).find(".tile-suffix-right").text(value.right.suffix);
  }

  configReceive(object, self, value, config) {
    if ("/img/static/icons/" + config.icon !== $(self).attr("src")) {
      $(self).find("img").fadeOut("fast", function() {
        $(this).attr("src", "/static/img/icons/" + config.icon).fadeIn("fast");
      });
    }
  }
}