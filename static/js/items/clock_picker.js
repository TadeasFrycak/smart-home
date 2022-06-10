"use strict";

class itemClockPicker {
  constructor() {
    this.type = "clock_picker";
  }

  setup(object) {
    let currentDate = new Date();
    object.find("input.clockpicker").clockpicker({
      default: currentDate.getHours() + ":" + currentDate.getMinutes(),
      placement: "auto",
      donetext: _("Done")
    });
  }

  valueReceive(object, self, value, config) {
    // TODO není vůbec hotové
    $(self).find("input.clockpicker").val(store(self, "value"));
  }

  valueTransmit(object) {
    object.find("input.clockpicker").change(function() {
      store($(this).closest(".modal-item"), "value", $(this).val()).trigger("value-transmit");
    });
  }

  configReceive(object, self, value, config) {
    $(self).find("input").attr("placeholder", config.placeholder);
  }
}