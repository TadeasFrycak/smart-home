// ----------------------------------------------
// Receive asynchronous communication
// ----------------------------------------------

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

socketio.on("slide_name_result", function(data){
  let chosen_slide_name_textbox = $($(".swiper-slide")[data.slide_index]).find(".swipe-header");
  $(chosen_slide_name_textbox).val(data.name);
});

socketio.on("modal_item_index_result", function(data){
  let old_index = data.old_index;
  let new_index = data.new_index;

  if (isModalOpen(null, data.tile_id)) {
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
});

socketio.on("modal_item_delete_result", function(data) {
  console.log(data.tile_id);
  console.log(data.id);

  if (isModalOpen(null, data.tile_id)) {
    let item = $(".modal_items_edit_sortable").find('.modal-edit-item[data-id="' + data.id+ '"]');
    // $(item).find(".modal-edit-item-dropdown").slideUp(function(){
    //   $(this).remove();
    // })
    // setTimeout(() => {
      $(item).slideUp(function() {
        $(this).remove();
      });
    // }, 500);

    $('.modal-item[data-id="' + data.id+ '"]').slideUp(function() {
      $(this).remove();
    });
  }
});

socketio.on("tile_delete_result", function(data){
  $(".tile[data-id="+data.tile_id+"]").parent().fadeOut(function() {$(this).remove()});
});

socketio.on("tile_icon_result", function(data){
  $(".tile[data-id="+data.tile_id+"] .tile-icon").attr("src", data.new_icon);
});

socketio.on("tile_type_result", function(data){
  if (isModalOpen("edit", data.tile_id)) {
    if (data.tile_values) {
      $(".tile-values-wrapper").empty().append(data.tile_values);
      initImages();
    }
  }

  $(".tile[data-id="+data.tile_id+"]").parent().replaceWith(data.tile_html);
  $(".tile[data-id="+data.tile_id+"]").each(function(){
    initializeHammerTile(this);
  });
});

socketio.on("tile_label_result", function(data){
  $(".tile[data-id="+data.tile_id+"] .tile-label").text(data.new_label);
});

socketio.on("tile_index_result", function(data){
  let old_index = data.old_index;
  let new_index = data.new_index;
  let slide_index = data.slide_index;

  // console.log({old_index,new_index,slide_index});

  let selected_slide = $(".swiper-slide")[slide_index];
  let all_tiles_within_slide = $(selected_slide).find(".grid-square");
  let selected_tile_old = all_tiles_within_slide[old_index];
  let selected_tile_new;

  let temporary_tile_old = $(selected_tile_old).clone();
  // let temporary_tile_new = $(selected_tile_new).clone();

  $(selected_tile_old).remove();

  if (new_index === all_tiles_within_slide.length) {
    selected_tile_new = all_tiles_within_slide[new_index-1];
    $(temporary_tile_old).insertAfter($(selected_tile_new));
  }
  else {
    selected_tile_new = all_tiles_within_slide[new_index];
    if (new_index>old_index) $(temporary_tile_old).insertAfter($(selected_tile_new));
    if (new_index<old_index) $(temporary_tile_old).insertBefore($(selected_tile_new));
  }
  // if (old_index == 0)
  // {
  // }
  // else
  // {
  //   $(selected_tile_new).replaceWith($(temporary_tile_old));
  //   $(selected_tile_old).replaceWith($(temporary_tile_new));
  // }
});

socketio.on("tile_id_result", function(data) {
  store($(".tile[data-id='"+data.tile_id+"']"), "id", data.new_id);
  $("#tile-mqtt-path").val("home/" + data.new_id);
  $(".modal-here").attr("data-tile-id", data.new_id);
  $('.modal-item[data-id="item-mqtt-path"]').each(function () {
    let itemID = store($(this), "value").split("/")[2];
    store($(this), "value", "home/" + data.new_id + "/" + itemID).trigger("value-receive");
  })
});

socketio.on("modal_item_prepend_result", function(data) {
  if (isModalOpen(null, data.tile_id)) {
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
      modalEditItemInit(this);
    });

    $(item).on("value-transmit", function() {
      modalDynamicValueSend(this);
    });
  }
});

socketio.on("get_add_tile_result", function(data) {
  let selected_slide = $($(".swiper-slide")[data.slide_index]).find(".add_new_tile_element");
  $(data.tile_html).insertBefore(selected_slide).hide().fadeIn();
  let tile_array = $($(".swiper-slide")[data.slide_index]).find(".grid-square");
  let appended_tile = $(tile_array[tile_array.length-1]);

  $(appended_tile).each(function(){
     console.log("Initializing");

     initializeHammerTile(this);
     $(this).removeAttr("style");
  });
});

socketio.on("get_normal_modal_result", function(data) {
  displayModal(data.modal, "normal", data.tile_id);

  // Initialise modal items
  $('.modal-item[data-group="modal-dynamic"]').on("value-transmit", function() {
    modalDynamicValueSend(this);
  });
});

socketio.on("doorbird_live_image", function(data) {
  $(".doorbird-live-image").attr("src", data.image);
  $(".doorbird-framerate").text(data.framerate + " " + _("FPS"));
});

socketio.on("doorbird_event", function() {
  if (store($(".modal-here"), "type") !== "doorbird") {
    socketio.emit("get_doorbird_modal", {"tab_id": sessionStorage.tabID});
  }
});
socketio.on("get_edit_modal_result", function(data) {
  console.log("Received edit modal");
  displayModal(data.modal, "edit", data.tile_id);

  initializeModalEditItems();
});

socketio.on("modal_item_id_result", function(data) {
  if (isModalOpen(null, data.tile_id)) {
    let obj = $('.modal-item[data-id="item-mqtt-path"][data-group="modal-edit-' + data.id + '"]');
    store(obj, "value", "home/" + data.tile_id + "/" + data.new_id).trigger("value-receive");

    store($(obj).closest(".modal-edit-item"), "id", data.new_id);
    store($('.modal-item[data-id="' + data.id + '"]'), "id", data.new_id)

    $('.modal-item[data-group="modal-edit-' + data.id + '"]').each(function(){
      store($(this), "group", "modal-edit-" + data.new_id);
    });
  }
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

socketio.on("slide_index_result", function() {
  store($(".swipe-body"), "index-change", true);
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
  console.log(data.slide_index);
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

  // if (isEditActive === "true") {
  //   $(".add_new_tile_element").hide().fadeIn(2000);
  //   $(".exit-edit-mode-button").hide().fadeIn(2000);

  //   // Připnutí Hammer pro každé "+" tlačítko
  //   $(".swiper-slide-active .add-new-tile-element").each(function() {
  //     let hammer = new Hammer(this);
  //     hammer.on("tap", function(el) {
  //       addNewTile();
  //     });
  //   });

    // lastSlide.find(".add_new_tile_element").each(function() {
    //   let hammer = new Hammer(this);

    //   hammer.on("tap", function() {
    //     addNewTile();
    //   });
    // });

    lastSlide.find(".swipe-header").each(function() {
      $( this ).prop("readonly",false)
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

// socketio.on("slide_prepend_result", function(data) {
//   swiper.prependSlide(data.slide);

//   let isEditActive = $(document.body).attr("data-is-edit-active");

//   if (isEditActive === "true") {
//     $(".add_new_tile_element").hide().fadeIn(2000);
//     $(".exit-edit-mode-button").hide().fadeIn(2000);

//     // Připnutí Hammer pro každé "+" tlačítko
//     $(".swiper-slide-active .add_new_tile_element").each(function() {
//       let hammer = new Hammer(this);
//       hammer.on("tap", function(el) {
//         addNewTile();
//       });
//     });

//     let lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
//     bindSortable(SortableTiles.length,lastSortablePage[lastSortablePage.length-1]);
//   }
// });

socketio.on("slide_prepend_animation_result", function() {
  swiper.slideTo(0, 1000);
});

// Asynchronous communication for tile
socketio.on("tile_value_result", function(data) {
  // Test each tile on the page
  let tileID = data.tile_id;
  let tileElement = $(".tile[data-id="+tileID+"]");
  let tileType = store(tileElement, "type");
  console.log("Tile_value_result event")

  // Tile type is toggle
  if (tileType === "toggle") {

    // console.log("Update Toggle")
    let tileStateLast = $(tileElement).find(".tile-status").text();
    let tileStateCurrent = data.value;
    // console.log("Last status: " + tileStateLast);
    // console.log("Current status: " + tileStateCurrent);
    // console.log($(tileElement));

    // Turn tile off
    if (tileStateLast.toLowerCase() === _("On").toLowerCase() && tileStateCurrent === 0) {
      $(tileElement).find(".tile-status").text(_("Off")); $(tileElement).toggleClass("tile-active");
      $(tileElement).find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");
    }
    // Turn tile on
    else if (tileStateLast.toLowerCase() === _("Off").toLowerCase() && tileStateCurrent === 1) {
      $(tileElement).find(".tile-status").text(_("On")); $(tileElement).toggleClass("tile-active");
      $(tileElement).find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
    }
  }
  // Tile type is value
  else if (tileType === "value") {
    tileElement.find(".tile-value-value").text(Math.round(data.value.value * 10) / 10);
    tileElement.find(".tile-value-suffix").text(data.value.suffix);
    tileElement.find(".tile-status").text(data.value.ago);
  }
  else if (tileType === "value_double") {
    tileElement.find(".tile-value-left").text(data.value.left.value);
    tileElement.find(".tile-value-right").text(data.value.right.value);
    tileElement.find(".tile-suffix-left").text(data.value.left.suffix);
    tileElement.find(".tile-suffix-right").text(data.value.right.suffix);
  }
  else if (tileType === "alarm_clock") {
    let tileActive = data.value.main;
    let tileId = data.tile_id;

    let tileMon = data.value.monday;
    let tileTue = data.value.tuesday;
    let tileWed = data.value.wednesday;
    let tileThu = data.value.thursday;
    let tileFri = data.value.friday;
    let tileSat = data.value.saturday;
    let tileSun = data.value.sunday;

    let tileElement = $(".tile[data-id="+tileId+"]");

    console.log(tileMon);
    // TODO:
    // tileActive = true;

    // tileMon = false;
    // tileTue = false;
    // tileWed = false;
    // tileThu = false;
    // tileFri = false;
    // tileSat = true;
    // tileSun = false;

    if (tileActive === true) {
      tileElement.toggleClass("tile-active",true);
    }
    else if (tileActive === false){
      tileElement.toggleClass("tile-active",false);
    }

    let tileDay = "Mon"
    if (tileMon === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileMon === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Tue"
    if (tileTue === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileTue === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Wed"
    if (tileWed === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileWed === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Thu"
    if (tileThu === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileThu === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Fri"
    if (tileFri === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileFri === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Sat"
    if (tileSat === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileSat === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
    tileDay = "Sun"
    if (tileSun === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
    else if (tileSun === false) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
  }
});

socketio.on("modal_item_config_result", function(data) {
  if (isModalOpen(null, data.tile_id)) {
    // TODO jen pokud je edit mód, tak dělat první řádek a pokud není, tak druhý
    store($('.modal-item[data-group="modal-edit-' + data.id + '"][data-id="' + data.value_name + '"]'), "value", data.new_value).trigger("value-receive");

    let currentItem = $('.modal-item[data-group="modal-dynamic"][data-id="' + data.id + '"], .modal-item[data-group="modal-preview"][data-id="' + data.id + '"]');
    let config = store(currentItem, "config");
    config[data.value_name] = data.new_value;
    store(currentItem, "config", config).trigger("config-receive");
  }
});

// Asynchronous communication for modal toggle
socketio.on("modal_item_value_result", function(data) {
  // If tile ID is same
  if (isModalOpen(null, data.tile_id)) {
    let item = $('.modal-item[data-id="' + data.id + '"][data-group="modal-dynamic"]');
    // If type of item is same
    if (store(item, "type") === data.type) {
      console.log(data.value);
      store(item, "value", data.value).trigger("value-receive");
    }
  }
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
    console.log("acom.js > something failed I guess");
  }
});

socketio.on("connect", function() {
  console.log("Client connected to server");
  let modalData = isModalOpen(null, null, true);
  if (modalData) {
    console.log("Opening", modalData);
    socketio.emit("get_"+modalData["type"]+"_modal", {"tile_id": modalData["tile_id"], "tab_id": sessionStorage.tabID})
  }
  $(".server-status").text(_("Online"));
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
  console.log("Client disconnected from server");

  $(".server-status").text(_("Offline"));

  if (store($(document.body), "is-edit-active") === true) {
    $(".bcg-normal").css({"opacity": 0, "transition": "0s all"});
    $(".bcg-edit").css({"opacity": 0.5, "transition": "0.5s all"});
  }
  else {
    $(".bcg-normal").css({"opacity": 0.4});
  }
});
