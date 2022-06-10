"use strict";

class itemDropdown {
  constructor() {
    this.type = "dropdown";

    $(document).click(e => {
      e.stopPropagation();
      if($('.select-menu').has(e.target).length === 0) {
        $('.select-menu').removeClass('open');
      }
    });
  }

  setup(object) {
    object.find('select[data-menu]').each(function() {
      let select = $(this),
        options = select.find('option'),
        menu = $('<div />').addClass('select-menu'),
        button = $('<div />').addClass('button'),
        list = $('<ul data-second="false"/>'),
        arrow = $('<em />').prependTo(button);

      options.each(function(i) {
        let option = $(this);
        list.append($('<li />').text(option.text()));
      });

      menu.css('--t', select.find(':selected').index() * -41 + 'px');
      select.wrap(menu);
      button.append(list).insertAfter(select);

      store(list.clone(), "second", true).insertAfter(button);
    });

    object.on('click', '.select-menu', function(e) {
      let menu = $(this);

      if(!menu.hasClass('open')) {
          menu.addClass('open');
      }
    });
  }

  valueReceive(object, self, value, config) {
    $(self).find('option').each(function (index){
      let menu = $(this).closest(".select-menu");
      let oldIndex = menu.find("option:selected").index();

      if ($(this).val() === value) {
        if (oldIndex !== index) {
          menu.addClass(index > oldIndex ? 'tilt-down' : 'tilt-up');
          menu.css('--t', index * -41 + 'px');
          $(this).attr("selected", true);
          setTimeout(() => {
            menu.removeClass('open tilt-up tilt-down');
          }, 500);
        }
      }
      else {
        $(this).attr("selected", false)
      }
    });
  }

  valueTransmit(object) {
    object.on('click', '.select-menu > ul > li', function(e) {

      let li = $(this),
          menu = li.parent().parent(),
          select = menu.children('select'),
          selected = select.find('option:selected'),
          index = li.index();

      menu.css('--t', index * -41 + 'px');
      selected.attr('selected', false);
      let newSelect = select.find('option').eq(index);
      newSelect.attr('selected', true);

      menu.addClass(index > selected.index() ? 'tilt-down' : 'tilt-up');

      setTimeout(() => {
          menu.removeClass('open tilt-up tilt-down');
      }, 500);
      store(object, "value", newSelect.text()).trigger("value-transmit");
    });
  }

  configReceive(object, self, value, config) {
    $(self).find("label").text(config.label);

    <!-- TODO config update for options-->
    function __configOptions(options) {
      if (options.length < config.options.length) {
        let newItem = options.last().clone().text(config.options[config.options.length-1]);
        newItem.insertAfter(options.last());
        return;
      }
      let cancelled = false;
      config.options.forEach(function(val, index) {
        if (cancelled === false) {
          if (val !== $(options[index]).text()) {
            if (options.length > config.options.length) {
              $(options[index]).remove();
              cancelled = true;
            }
            else {
              $(options[index]).text(val);
            }
          }
        }
      });
    }

    __configOptions($(self).find('ul[data-second="false"]').find("li"));
    __configOptions($(self).find('ul[data-second="true"]').find("li"));
    __configOptions($(self).find("option"));

  }
}