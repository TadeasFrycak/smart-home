"use strict";

class itemIconPicker {
  constructor() {
    this.type = "icon_picker";
  }

  setup(object) {}

  valueReceive(object, self, value, config) {
    $(".modal-edit-icon").removeClass("modal-edit-icon-active");
    $(self).find("img[data-name='" + value + "']").addClass("modal-edit-icon-active");
  }

  valueTransmit(object) {
    object.find(".modal-edit-icon").each(function() {
      Hammer(this).on("tap", function(elem) {
        $(".modal-edit-icon").removeClass("modal-edit-icon-active");  // TODO chybí this, ... udělá se u všech - problém !
        $(elem.target).addClass("modal-edit-icon-active");
        store(object, "value", store(elem.target, "name")).trigger("value-transmit");
      });
    });
  }

  configReceive(object, self, value, config) {}
}