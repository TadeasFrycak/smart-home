"use strict";

class tilePrusa {
  constructor() {
    this.type = "prusa";
  }

  setup(object) {}

  tap(object, self, config) {}

  valueReceive(object, self, value, config) {
    $(".prusa-progress-bar-current").css("width", value.percentage + "px");
    $(".prusa-percentage").text(value.percentage);
    $(".prusa-time").text(value.time);
    $(".prusa-hotend").text(value.hotend);
    $(".prusa-bed").text(value.bed);
    $(".prusa-status").text(value.status);
  }

  configReceive(object, self, value, config) {
    if ("/img/static/icons/" + config.icon !== $(self).attr("src")) {
      $(self).find("img").fadeOut("fast", function() {
        $(this).attr("src", "/static/img/icons/" + config.icon).fadeIn("fast");
      });
    }
  }
}