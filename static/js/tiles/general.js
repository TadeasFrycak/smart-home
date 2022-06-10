"use strict";

let tileObjects = [
  new tileValueDouble(),
  new tileAlarmClock(),
  new tileToggle(),
  new tilePrusa(),
  new tileValue()
]

function tile(object) {
  let type = store(object, "type");

  tileObjects.forEach(function(val, index) {
    if (val.type === type) {
      val.setup(object);

      $(object).on("value-receive", function() {
        let value = store(this, "value");
        let config = store(this, "config");
        val.valueReceive(object, this, value, config);
      });

      $(object).on("config-receive", function() {
        // TODO zde se updatne label
        let value = store(this, "value");
        let config = store(this, "config");
        val.configReceive(object, this, value, config);
      });

      $(object).on("tap", function() {
        let config = store(this, "config");
        val.tap(object, this, config);
      });
    }
  });
}