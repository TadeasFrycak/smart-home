"use strict";

let itemObjects;

$(document).ready(function(){
  itemObjects = [
    new itemDateRangePicker(),
    new itemButtonGroup(),
    new itemClockPicker(),
    new itemProgressBar(),
    new itemIconPicker(),
    new itemDropdown(),
    new itemButton(),
    new itemSlider(),
    new itemToggle(),
    new itemGraph(),
    new itemInput(),
    new itemImage()
  ]
});

function item(object) {
  let type = store(object, "type");

  itemObjects.forEach(function(val, index) {
    if (val.type === type) {
      val.setup(object);
      val.valueTransmit(object);

      $(object).on("value-receive", function() {
        let value = store(this, "value");
        let config = store(this, "config");
        val.valueReceive(object, this, value, config);
      });

      $(object).on("config-receive", function() {
        let value = store(this, "value");
        let config = store(this, "config");
        val.configReceive(object, this, value, config);
      });
    }
  });
}