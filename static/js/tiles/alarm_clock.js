"use strict";

class tileAlarmClock {
  constructor() {
    this.type = "alarm_clock";
  }

  setup(object) {}

  tap(object, self, config) {
    store(self, "value", {
          "main":      !$(self).find(".tile").hasClass("tile-active"),
          "monday":     $(self).find(".ac-glyph[data-type='monday']")   .hasClass("ac-glyph-active"),
          "tuesday":    $(self).find(".ac-glyph[data-type='tuesday']")  .hasClass("ac-glyph-active"),
          "wednesday":  $(self).find(".ac-glyph[data-type='wednesday']").hasClass("ac-glyph-active"),
          "thursday":   $(self).find(".ac-glyph[data-type='thursday']") .hasClass("ac-glyph-active"),
          "friday":     $(self).find(".ac-glyph[data-type='friday']")   .hasClass("ac-glyph-active"),
          "saturday":   $(self).find(".ac-glyph[data-type='saturday']") .hasClass("ac-glyph-active"),
          "sunday":     $(self).find(".ac-glyph[data-type='sunday']")   .hasClass("ac-glyph-active")
        }).trigger("value-transmit");
  }

  valueReceive(object, self, value, config) {
    for (let key in value) {
      let currentValue = value[key];
      if (key === "main"){
        $(self).find(".tile").toggleClass("tile-active", currentValue);
      }
      else $(self).find(".ac-glyph[data-type=" + key + "]").toggleClass("ac-glyph-active", currentValue);
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