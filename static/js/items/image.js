"use strict";

class itemImage {
  constructor() {
    this.type = "image";
  }

  setup(object) {
    object.on("click", function() {
      $(this).find(".live-image").toggleClass("live-image-active");
    });

  }

  valueReceive(object, self, value) {
    $(self).find(".live-image").attr("src", value);
  }

  valueTransmit(object) {}

  configReceive(object, self, value, config) {}
}