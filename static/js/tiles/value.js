"use strict";

class tileValue {
  constructor() {
    this.type = "value";
  }

  setup(object) {}

  tap(object, self, config) {}

  valueReceive(object, self, value, config) {
    $(self).find(".tile-value-value").text(Math.round(value.value * 10) / 10);  // TODO není hezké úplně všude, není elegantní
    $(self).find(".tile-value-suffix").text(value.suffix);
    $(self).find(".tile-status").text(value.ago);
  }

  configReceive(object, self, value, config) {}
}