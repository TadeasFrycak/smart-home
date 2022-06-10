"use strict";

// TODO input - dodělat animaci sliding up při mazání u list inputu
// TODO qol bug - když rychle zanču klikat na input - tlačítko add (pokud je input list), tak se to tam hodně špatně nastackuje, řešení??

class itemInput {
  constructor() {
    this.type = "input";
  }

  setup(object) {
    object.find(".modal-input").keydown(function(event){
      event.keyCode===13 && $(object).find(".submit").click();
    });
  }

  valueReceive(object, self, value, config) {
    if (config.list === true) {
      if (config.count == 1) {  // TODO count is not number (bcs of input => input number - output type = int
        value.forEach(function(val, index) {
          value[index] = [val];
        });
      }

      let inputs = object.find(".input-group");

      // Add input group
      if (inputs.length < value.length) {
        let element = object.find(".input-group").last();
        element.clone().insertAfter(element);
        let last = object.find(".input-group").last().hide().slideDown();
        last.find("input").val("").attr("placeholder", _("N/A"));
      }

      // Remove input group
      else if (value.length < inputs.length) {
        let removed = false;
        inputs.each(function(index) {
          let inputGroup = $(this);

          inputGroup.find("input").each(function(innerIndex) {
            try {
              if ($(this).val() !== value[index][innerIndex] && !removed) {
                removed = true;
                inputGroup.remove();
              }
            }
            catch (e) {}
          });
        });

        if (!removed) {
          inputs.last().closest(".input-group").remove();
        }
      }

      // Changing value
      else {
        inputs.each(function(index) {
          let inputGroup = $(this);

          inputGroup.find("input").each(function(innerIndex) {
            $(this).val(value[index][innerIndex]);
          });
        });
      }

      // Disable delete button if length <= 1
      object.find(".input-group-append").find("button").prop("disabled", object.find(".input-group").length <= 1)
    }
    else {
      if (config.count === 1 || config.count === undefined) {
        value = [value];
      }
      $(self).find("input").each(function(innerIndex) {
        $(this).val(value[innerIndex]);
      });
    }
  }

  send(object) {
    let config = store(object, "config");
    let values = [];

    // For every input group
    object.find(".input-group").each(function (index){
      // If not multiple input
      if (config.count == 1) {  // TODO count is string
        values.push($(this).find("input").val());
      }
      else {
        values.push([]);
        // For every input
        $(this).find("input").each(function (){
          values[index].push($(this).val());
        });
      }
    });

    // If not input type list
    if (config.list === false) values = values[0];
    store(object, "value", values).trigger("value-transmit");
  }

  valueTransmit(object) {
    let self = this;

    // Input list - clink on add button
    object.on("click", ".add-input", function() {
      // TODO tohle je duplicitní
      let element = object.find(".input-group").last();
      element.clone().insertAfter(element);
      object.find(".input-group").last().hide().slideDown().find("input").val("").attr("placeholder", _("N/A"));

      self.send(object);
    });

    // Input list - clink on remove button
    object.on("click", ".remove-input", function() {
      if (object.find(".input-group").length > 1) {
        $(this).closest(".input-group").remove();
        self.send(object);
      }
    });

    // Input on input event
    object.on("input", "input", function() {
      let config = store(object, "config");
      object.find("button").prop("disabled", false);

      if (config.button !== true) {
        self.send(object);
      }
    });

    // Input with confirm button - on blur
    // object.find("input").blur(function() {
    //   let config = store(object, "config");
    //
    //   if (config.button === true) {
    //     object.find(".submit").prop("disabled", true);
    //     self.send(object);
    //   }
    // });

    // Input with confirm button - on submit click
    object.on("click", ".submit", function() {
      $(this).prop("disabled", true);
      self.send(object);
    });
  }

  configReceive(object, self, value, config) {
    // Velké todo here - na všechnmo - append, prepend, count, number, invalid (tohle dát - pokud je input invalid, tak neposlat), ........
    // Při přeměnách --list --count se vloží vždy do prvního ['']
    $(self).find("label").text(config.label);
    $(self).find("input").prop("readonly", config.readonly);
    // Todo placeholde potřebuje na tu automatickou část refresh
    if (config.placeholder === "") config.placeholder = _("N/A");
    $(self).find("input").attr("placeholder", config.placeholder);
    $(self).find("input").toggleClass("is-invalid", config.invalid);

    // Prepend box
    if (config.prepend !== "" && typeof config.prepend !== 'undefined') {
      if ($(self).find(".input-group-prepend").length === 0) {
        // TODO vyřešit jinak, tohle dvojí html je špatně
        $('<div class="input-group-prepend"><span class="input-group-text"></span></div>').insertBefore($(self).find("input"));
      }
      $(self).find(".input-group-prepend").find(".input-group-text").text(config.prepend);
    }
    else {
      $(self).find(".input-group-prepend").remove();
    }
    // Append button
    if (config.button) {
      if ($(self).find(".input-group-append").length === 0) {
        $('<div class="input-group-append"><button class="submit btn btn-sm {% if mode == "light" %}btn-outline-dark{% else %}btn-outline-light{% endif %}" type="button" disabled>{{ _("Submit") }}</button></div>').insertAfter($(self).find("input"));
      }
    }
    else if (!config.list) {
      $(self).find(".input-group-append").remove();
    }

    $(self).find("input").attr("type", config.number ? "number" : "text")
  }
}