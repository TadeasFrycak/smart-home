"use strict";

class tileToggle {
  constructor() {
    this.type = "toggle";
  }

  setup(object) {}

  tap(object, self, config) {
    let value = !$(self).find(".tile").hasClass("tile-active");
    store(self, "value", value).trigger("value-transmit");
  }

  valueReceive(object, self, value, config) {
    // Turn tile on
    if (value === true) {
      $(self).find(".tile-status").text(_("On"));
      $(self).find(".toggle-dot").css("background-color", "rgba(0, 196, 42, 0.28)");
      $(self).find(".tile").addClass("tile-active");
    }
    // Turn tile off
    else if (value === false) {
      $(self).find(".tile-status").text(_("Off"));
      $(self).find(".toggle-dot").css("background-color", "rgba(255, 0, 0, 0.28)");  // TODO tohle půjde do class, JS bude akorát switchovat classy
      $(self).find(".tile").removeClass("tile-active");
    }
  }

  configReceive(object, self, value, config) {
    if ("/img/static/icons/" + config.icon !== $(self).attr("src")) {
      $(self).find("img").fadeOut("fast", function() {
        $(this).attr("src", "/static/img/icons/" + config.icon).fadeIn("fast");
      });
    }
  }
}