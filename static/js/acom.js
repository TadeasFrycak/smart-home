// ----------------------------------------------
// Receive asynchronous communication
// ----------------------------------------------

socketio = io("/com", {
  forceNew: true,
  reconnectionDelay: 100,
  reconnectionDelayMax: 500
});
reconnected = false;


// setTimeout(function(){
//   vibrate = navigator.vibrate ? 'vibrate' : navigator.webkitVibrate ? 'webkitVibrate' : null;
// }, 1000);

let serverModalOpened = false;

function serverModal(header, message, button=_("Reload"), command="reload") {
    $("#my-modal").hide();
    $(".modal-here").empty();
    $(".modal-here").append('<div class="modal fade" id="modal-server" tabindex="-1" role="dialog" aria-hidden="true"> <div class="modal-dialog modal-dialog-centered" role="document"> <div class="modal-content"> <div class="modal-header"> <h5 class="modal-title" id="exampleModalLongTitle">' + header + '</h5> </div> <div class="modal-body">' + message + '</div> <div class="modal-footer"> <button type="button" class="btn btn-danger ' + command +'">' + button + '</button></div></div></div></div>');
    // navigator[vibrate](50);
    $("#modal-server").modal({backdrop: "static", keyboard: false});
}

// Reload page
socketio.on("reload", function() {
  console.log("Server command: reload");
  location.reload();
});

socketio.on("reconnect", function() {
  console.log("Server reconnected! Reloading...");
  location.reload();
});

// Asynchronous communication for global notifications
audio = new Audio("/static/sound/beep.mp3");
socketio.on("notify", function(msg) {
  wait = false;
  audio.play();
  notify(_(msg.title), _(msg.message), msg.type, msg.delay);
});

$(document.body).on("click", ".reload", function() {
  location.reload();
});


// Tile sync
socketio.on("tile_delete_result", function(data){
  $(".tile-item[data-id='"+data.tile_id+"']").show().toggle("slide:right").removeAttr("style");
  setTimeout(() => {$(".tile-item[data-id='"+data.tile_id+"']").remove()}, 600)

  if (isModalOpen("edit", data.tile_id)) {
    $('#my-modal').modal('hide');
  }
});

socketio.on("tile_config_result", function(data){
  if (isModalOpen("edit", data.tile_id)) {
    store($('.modal-item[data-group="tile-dynamic"][data-id=' + data.value_name +']'), "value", data.value).trigger("value-receive");
  }
  let tile = $('.tile-item[data-id="' + data.tile_id +'"]');
  let config = store(tile, "config");
  config[data.value_name] = data.value;
  store(tile, "config", config).trigger("config-receive");
});

socketio.on("tile_type_result", function(data){
  if (isModalOpen("edit", data.tile_id)) {
    store($('.modal-item[data-group="tile"][data-id="type"]'), "value", data.type)

    if (data.tile_protocol_btns) {
      $(".tile-protocol-btns").slideDown().empty().append(data.tile_protocol_btns);
      $('.modal-item[data-group="tile"][data-id="protocol-btn"]').on("value-transmit", function() {
        tileProtocol(this);
      });

    }
    else {
      $(".tile-protocol-btns").slideUp();
    }

    if (data.tile_values) {
      if ($("#tile-dynamic-values").is(":hidden")) {
        $(".tile-values-wrapper").append(data.tile_values);
        $("#tile-dynamic-values").slideDown();
        initializeTileDynamic();
      }
      else {
        $(".tile-values-wrapper").slideUp(function() {
          $(".tile-values-wrapper").empty().append(data.tile_values).slideDown();
          initializeTileDynamic();
        });
      }
    }
    else if (data.tile_values !== false) {
      $("#tile-dynamic-values").slideUp(function() {
        $(".tile-values-wrapper").empty();
      });
    }
  }

  $(".tile-item[data-id='"+data.tile_id+"']").replaceWith(data.tile_html)
  $(".tile-item[data-id='"+data.tile_id+"']").each(function() {
    initializeHammerTile(this);
  });

  tileValueTransmit($(".tile-item[data-id='"+data.tile_id+"']"));

});

socketio.on("tile_label_result", function(data){
  $(".tile-item[data-id='"+data.tile_id+"'] .tile-label").text(data.new_label);
  if (!data.tile_only) {
    if (isModalOpen("edit", data.tile_id)) {
      $("#tile_name").val(data.new_label);
    }
  }
});

socketio.on("tile_index_result", function(data){
  let old_index = data.old_index;
  let new_index = data.new_index;
  let slide_index = data.slide_index;

  let selected_slide = $(".swiper-slide")[slide_index];
  let all_tiles_within_slide = $(selected_slide).find(".tile-item");
  let selected_tile_old = all_tiles_within_slide[old_index];
  let selected_tile_new;

  let temporary_tile_old = $(selected_tile_old).clone();

  $(selected_tile_old).remove();

  if (new_index === all_tiles_within_slide.length) {
    selected_tile_new = all_tiles_within_slide[new_index-1];
    $(temporary_tile_old).insertAfter($(selected_tile_new));
  }
  else {
    selected_tile_new = all_tiles_within_slide[new_index];
    if (new_index>old_index) $(temporary_tile_old).insertAfter($(selected_tile_new));;
    if (new_index<old_index) $(temporary_tile_old).insertBefore($(selected_tile_new));
  }
});

socketio.on("tile_value_result", function(data) {
  let tile = $('.tile-item[data-id="' + data.tile_id + '"]');
  store(tile, "value", data.value).trigger("value-receive");
});

socketio.on("tile_protocol_values_result", function(data) {
  if(isModalOpen("edit", data.tile_id)) {
    store($("fieldset[data-type='" + data.protocol + "'][data-id='" + data.tile_id + "']").find('.modal-item[data-group="protocol-tile"][data-id="' + data.value_name + '"]'), "value", data.value).trigger("value-receive");
  }
});

socketio.on("tile_protocol_result", function(data) {
  if(isModalOpen("edit", data.tile_id)) {

    store($('.modal-item[data-group="tile"][data-id="protocol-btn"]'), "value", data.protocols).trigger("value-receive");
    if (data.state === "add") {
      $(".tile-protocols-wrapper").append(data.html);
      $(".tile-protocols-wrapper").find("fieldset[data-type='" + data.new_protocol + "']").hide().slideDown().find('.modal-item[data-group="protocol-tile"]').on("value-transmit", function() {
        tileProtocolInit(this);
      });
    }

    else if (data.state === "remove") {
      // $("#tile-protocol").find("label[data-type='" + data.new_protocol +"']").removeClass("active");
      let section = $(".tile-protocols-wrapper").find("fieldset[data-type='" + data.new_protocol + "']");
      section.slideUp(function () {
        $(this).remove();
      })
    }
  }
});

socketio.on("modal_item_protocol_values_result", function(data) {
  if(isModalOpen("edit", data.tile_id)) {
    store($("fieldset[data-type='" + data.protocol + "'][data-id='" + data.id + "']").find('.modal-item[data-group^="protocol-item-"][data-id="' + data.value_name + '"]'), "value", data.value).trigger("value-receive");
  }
});

socketio.on("modal_item_protocol_result", function(data) {
  if(isModalOpen("edit", data.tile_id)) {
    store($('.modal-item[data-group="item-protocol-btn"][data-id="' + data.id + '"]'), "value", data.protocols).trigger("value-receive");

    if (data.state === "add") {
      $(".item-protocols-wrapper[data-id='" + data.id + "']").append(data.html);
      $(".item-protocols-wrapper").find("fieldset[data-type='" + data.new_protocol + "'][data-id='" + data.id + "']").hide().slideDown().find('.modal-item[data-group^="protocol-item-"]').on("value-transmit", function() {
        modalItemProtocolInit(this);
      });
      $('.modal-item[data-group^="protocol-item-"]').on("value-transmit", function() {
        modalItemProtocolInit(this);
      });
    }

    else if (data.state === "remove") {
      let section = $(".item-protocols-wrapper").find("fieldset[data-type='" + data.new_protocol + "'][data-id='" + data.id + "']");
      section.slideUp(function () {
        $(this).remove();
      })
    }
  }
});


// Showing modals
socketio.on("get_normal_modal_result", function(data) {
  displayModal(data.modal, "normal", data.tile_id);

  // Initialise modal items
  $('.modal-item[data-group="modal-dynamic"]').on("value-transmit", function() {
    modalDynamicValueSend(this);
  });
});

socketio.on("get_edit_modal_result", function(data) {
  displayModal(data.modal, "edit", data.tile_id);

  initializeModalEditItems();
});

socketio.on("get_settings_modal_result", function(data) {
  // ( > events.js )
  displayModal(data.modal, "settings");

  $(".modal-settings-page-appearance").click(function() {
    let change_to = store($(this), "type");
    socketio.emit("user_mode", {"mode": change_to});
    console.log("Change appearance to " + change_to);
  });

  $(".background-type").on("click", "input",  function() {
    // ( > modal_edit_events.js )
    let typeName = store($(this), "type");
    console.log("Background:", typeName);
    if (typeName !== "static") {
      $(".fotorama").slideUp();
      socketio.emit("user_background", {"background": typeName});
    }
    else {
      $(".fotorama").slideDown();
    }
  });

  $('.fotorama')
    .on('fotorama:showend ',  // Stage image of some frame is loaded
      function (e, fotorama, extra) {
        // console.log('## ' + e.type);
        // console.log('active frame', fotorama.activeFrame);
        // console.log('additional data', extra);
        let background = fotorama.activeFrame.img.split("/");
        socketio.emit("user_background", {"background": background[background.length-1]})
      }
    )
    // Initialize fotorama manually
    .fotorama({
      allowfullscreen: true,
      nav: "thumbs",
      keyboard: {"home": true, "end": true},
  });
});

socketio.on("get_client_list_modal_result", function(data) {
  // ( > events.js )
  displayModal(data.modal, "client_list");
});

socketio.on("get_user_list_modal_result", function(data) {
  // ( > events.js )
  displayModal(data.modal, "user_list");
});

socketio.on("get_doorbird_modal_result", function(data) {
  // ( > events.js )
  // TODO sjednotit modaly do jednoho výslendého eventu
  displayModal(data.modal, "doorbird");
});

socketio.on("get_android_modal_result", function(data) {
  displayModal(data.modal, "android");
});

socketio.on("get_add_tile_result", function(data) {
  let selectedSlide = $($(".swiper-slide")[data.slide_index]);
  let selectedBtn = selectedSlide.find(".add_new_tile_element");
  $(data.tile_html).insertBefore(selectedBtn)
  let tile_array = $($(".swiper-slide")[data.slide_index]).find(".tile-item");
  let appended_tile = $(tile_array[tile_array.length-1]);

  let isEditActive = store($(document.body), "is-edit-active");

  $(appended_tile).each(function(){
    initializeHammerTile(this);
  });

  // Animation
  if (isEditActive === true) {
    appended_tile.hide();
    selectedBtn.removeClass("add-tile-alpha").css({"transform": "scale(1)"})


    setTimeout(() => {
      // New line must have special animation - to prevent foul blink
      if ((selectedSlide.find(".tile-item").length-1) % howMany === howMany -1) {
          appended_tile.show();
          selectedBtn.addClass("add-tile-alpha").removeAttr("style").css("transition", "none").hide().fadeIn(function () {
            $(this).removeAttr("style");
          });
      }
      else {
        appended_tile.hide().toggle("slide:left").removeAttr("style");
        selectedBtn.addClass("add-tile-alpha").removeAttr("style");
      }
    }, 500);

  }
  else {
    appended_tile.hide().toggle("slide:left").removeAttr("style");
  }

});


// Modal sync
socketio.on("modal_item_prepend_result", function(data) {
  if (isModalOpen(null, data.tile_id)) {
    // TODO rozdělit na normal dynamic modal a na edit modal
    let fieldset = $(data.fieldset);
    let item = $(data.item);

    $(".modal_items_edit_sortable").prepend(fieldset);
    $(".modal-dynamic").prepend(item);

    $(fieldset).hide().slideDown();
    $(item).hide().slideDown();

    $(fieldset).find(".modal-edit-item-delete").on("click",function(e){
      modalEditItemDelete(this);
    });
    $(fieldset).find('.modal-item[data-group^="modal-edit-"]').on("value-transmit", function(event) {
      modalEditItemTextChanged(this);
    });

    $(item).on("value-transmit", function() {
      modalDynamicValueSend(this);
    });
    $(fieldset).find('.modal-item[data-group="item-protocol-btn"]').on("value-transmit", function() {
      modalItemProtocol(this);
    });
  }
});

socketio.on("modal_item_index_result", function(data){
  let old_index = data.old_index;
  let new_index = data.new_index;

  if (isModalOpen("edit", data.tile_id)) {
    let all_tiles_within_slide = $(".modal_items_edit_sortable").find(".modal-edit-item");
    let selected_item_old = all_tiles_within_slide[old_index];
    let selected_item_new;

    let temporary_item_old = $(selected_item_old).clone();

    $(selected_item_old).remove();

    if (new_index === all_tiles_within_slide.length) {
      selected_item_new = all_tiles_within_slide[new_index - 1];
      $(temporary_item_old).insertAfter($(selected_item_new));
    } else {
      selected_item_new = all_tiles_within_slide[new_index];
      if (new_index > old_index) $(temporary_item_old).insertAfter($(selected_item_new));
      if (new_index < old_index) $(temporary_item_old).insertBefore($(selected_item_new));
    }
  }

  else if (isModalOpen("normal", data.tile_id)) {
    let items = $(".modal-item[data-group='modal-dynamic']");  // [data-id='" + data.id + "']
    let selected_item_old = items[old_index];
    let selected_item_new;

    let temporary_item_old = $(selected_item_old).clone();

    $(selected_item_old).remove();

    if (new_index === items.length) {
      selected_item_new = items[new_index - 1];
      $(temporary_item_old).insertAfter($(selected_item_new));
    } else {
      selected_item_new = items[new_index];
      if (new_index > old_index) $(temporary_item_old).insertAfter($(selected_item_new));
      if (new_index < old_index) $(temporary_item_old).insertBefore($(selected_item_new));
    }
    let testItem = $($(".modal-item[data-group='modal-dynamic']")[new_index]);
    console.log(testItem);
    item(testItem);
    $(testItem).on("value-transmit", function() {
      modalDynamicValueSend(this);
    });
  }
});

socketio.on("modal_item_delete_result", function(data) {
  console.log(data.tile_id);
  console.log(data.id);

  if (isModalOpen(null, data.tile_id)) {
    let item = $(".modal_items_edit_sortable").find('.modal-edit-item[data-id="' + data.id+ '"]');
      $(item).slideUp(function() {
        $(this).remove();
      });

    $('.modal-item[data-id="' + data.id+ '"]').slideUp(function() {
      $(this).remove();
    });
  }
});

socketio.on("modal_item_config_result", function(data) {
  function save(currentItem) {
    let config = store(currentItem, "config");
    config[data.value_name] = data.new_value;
    store(currentItem, "config", config).trigger("config-receive");
  }

  if (isModalOpen("normal", data.tile_id)) {
    save($('.modal-item[data-group="modal-dynamic"][data-id="' + data.id + '"]'));
  }

  else if (isModalOpen("edit", data.tile_id)) {
    // Update label text in header of item
    if (data.value_name === "label") {
      $(".item-label[data-id='" + data.id +"']").text(data.new_value)
    }

    // Update preview
    save($('.modal-item[data-group="modal-fieldset"][data-id="' + data.id + '"]'));

    // Update config items - if I am not sender
    if (!data.preview_only) {
      store($('.modal-item[data-group="modal-edit-' + data.id + '"][data-id="' + data.value_name + '"]'), "value", data.new_value).trigger("value-receive");
    }
  }
});

socketio.on("modal_item_value_result", function(data) {
  // If tile ID is same
  if (isModalOpen(null, data.tile_id)) {
    let item = $('.modal-item[data-id="' + data.id + '"][data-group="modal-dynamic"]');
    // If type of item is same
    store(item, "value", data.value).trigger("value-receive");
  }
});


// Modal settings sync
socketio.on("user_mode_result", function(data) {
  if (data.mode === "light") {
    $(document.body).removeClass("dark").addClass("light");
    $(".add-img").attr("src", "img/static/add/light.png");
  }
  else if (data.mode === "dark") {
    $(document.body).removeClass("light").addClass("dark");
    $(".add-img").attr("src", "img/static/add/dark.png");
  }
});

socketio.on("user_background_result", function(data) {
  console.log(data.background);
  $("<div class='bcg-new bcg-normal'></div>").insertBefore(".bcg-old");
  $(".bcg-new").css("background-image", "url(img/backgrounds/" + data.background + ")");
  let tmpImg = new Image() ;
  tmpImg.src = "img/backgrounds/" + data.background
  tmpImg.onload = function() {
    $(".bcg-old").fadeOut(2000, function() {
      this.remove();
      $(".bcg-normal").removeClass("bcg-new").addClass("bcg-old");
    });
  };
});


// Doorbird sync
socketio.on("doorbird_live_image", function(data) {
  if (isModalOpen("doorbird")) {
    $(".doorbird-live-image").attr("src", data.image);
    $(".doorbird-framerate").text(data.framerate + " " + _("FPS"));
  }
});



let audioContext = new AudioContext();



function onError(e) {
    console.log(e);
}


socketio.on("doorbird_audio", function(data) {
  console.log(data)
  audioContext.decodeAudioData(data, function (buffer) {
      console.log(buffer);
  }, onError);

});

socketio.on("doorbird_event", function() {
  if (store($(".modal-here"), "type") !== "doorbird") {
    socketio.emit("get_doorbird_modal", {"tab_id": sessionStorage.tabID});
  }
});

// Slide sync
socketio.on("slide_index_result", function() {
  store($(".swipe-body"), "index-change", true);
});

socketio.on("slide_name_result", function(data){
  let chosen_slide_name_textbox = $($(".swiper-slide")[data.slide_index]).find(".swipe-header");
  $(chosen_slide_name_textbox).val(data.name);
});

socketio.on("slide_delete_result", function(data) {
  let index = data.index;

  if (index === swiper.realIndex) {
    if (index === 0) swiper.slideTo(index+1, 1000);
    else swiper.slideTo(index-1, 1000);
    setTimeout(() => {swiper.removeSlide(index);}, 1000);
  }
  else {
    swiper.removeSlide(index);
  }
});

socketio.on("slide_append_result", function(data) {
  swiper.addSlide(data.slide_index, data.slide);

  // let isEditActive = store($(document.body), "is-edit-active");

  let lastSlide = $($(".swiper-slide")[data.slide_index]);

  $(lastSlide).find(".dropdown").on("show.bs.dropdown", function(){
    showDropdown(this);
  });

  $(lastSlide).find(".dropdown").on("hide.bs.dropdown", function(e){
    hideDropdown(this, e);
  });
  lastSlide.find(".tile").each(function(){
    initializeHammerTile(this);
  });

  lastSlide.find(".swipe-header").on("input", function(){
    let nameOfPageChanged = $(this).val();
    socketio.emit("slide_name", {"index": swiper.realIndex, "new_name": nameOfPageChanged});
  });

  if (swiper.realIndex === data.slide_index) {
    swiper.slideTo(data.slide_index+1, 0);
  }

    lastSlide.find(".swipe-header").each(function() {
      $(this).prop("disabled",false).removeClass("unselectable");
      // $( this ).css({"border-bottom-width":"1px","border-bottom-style":"solid","width":"fit-content"});
    });

    $(".exit-edit-mode-button").hide().fadeIn(2000);

    let lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
    bindSortable(SortableTiles.length,lastSortablePage[data.slide_index]);
    resize();
  // }
});

socketio.on("slide_append_animation_result", function(data) {
  swiper.slideTo(data.slide_index, 1000);
});


// Renew
socketio.on("graph_rwr", function(data) {
  // if (modal_caller_id === msg.id_tile) {
  try {
    for (let i = 0; i < graphs_id.length; i++) {

      if (graphs_id[i] === data.graph_id) {  // Shodné ID
        console.log("Found my graph");
        // addGraphData(graphs[i],msg.data_x,msg.data_y);
        // addGraphData(graphs[i],msg.data_x,msg.data_y);
        graphs[i].data.datasets[0].data = data.value.y;
        graphs[i].data.labels = data.value.x;
        graphs[i].update();
        // websiteChart.update();
      }
    }
  }
  catch {
    console.error("acom.js > something failed I guess");
  }
});


// Client
socketio.on("connect", function() {
  // console.info("Client connected to server");
  if (reconnected) {
    console.info("Client reconnected to the server");
    location.reload()
  }
  else{
    let modalData = isModalOpen(null, null, true);
    if (modalData) {
      socketio.emit("get_"+modalData["type"]+"_modal", {"tile_id": modalData["tile_id"], "tab_id": sessionStorage.tabID})
    }
    $(".server-status").text(_("Online"));
  }
});
  let ping_pong_times = [];
  let start_time;

  function sendPing() {
    start_time = (new Date).getTime();
    socketio.emit("my-ping");
  }

  window.setTimeout(function() {
    sendPing();
  }, 5000);

  window.setInterval(function() {
    sendPing();
  }, 10000);

  // Handler for the "pong" message. When the pong is received, the
  // time from the ping is stored, and the average of the last 30
  // samples is average and displayed.
  socketio.on("my-pong", function() {
    let latency = (new Date).getTime() - start_time;
    ping_pong_times.push(latency);
    ping_pong_times = ping_pong_times.slice(-10); // keep last 30 samples
    let sum = 0;
    for (let i = 0; i < ping_pong_times.length; i++)
      sum += ping_pong_times[i];
    let myPing = Math.round(sum / ping_pong_times.length);
    if (myPing >= 1000) myPing = parseFloat((myPing/1000).toFixed(2)) + " s";
    else myPing = myPing + " ms"
    $(".server-status").text(myPing);
  });

socketio.on("disconnect", function() {
  $(".server-status").text(_("Offline"));

  if (!serverModalOpened) {
    document.title = _("Offline") + " | " + _("SH");
    setTimeout(() => {
      console.log("Client disconnected from server");
      reconnected = true;
      serverModal(_("Offline"), _("Server is now offline. The page will be auto-reloaded after server will be online. If you think that this message is wrong or this is a bug, you can reload page manually."));
      }, 1000);
  }
});
