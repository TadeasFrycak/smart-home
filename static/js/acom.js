$(document).ready(function(){
  // ----------------------------------------------
  // Receive asynchronous communication
  // ----------------------------------------------

  // Initialise communication
  socketio = io("/com");

  socketio.on("user_mode_result", function(data) {
    if (data.mode === "light") {
      $("body").removeClass("dark").addClass("light");
      $(".add-img").attr("src","img/static/add.png");
      $(".page_settings_icon").attr("src","img/static/settings.png");
    }
    else if (data.mode === "dark") {
      $("body").removeClass("light").addClass("dark");
      $(".add-img").attr("src","img/static/add-dark.png");
      // $(".page_settings_icon").attr("src","img/static/settings-dark.png");
    }
  });

  socketio.on("slide_name_result", function(data){
    let chosen_slide_name_textbox = $($(".swiper-slide")[data.slide_index]).find(".swipe-header-textbox");
    $(chosen_slide_name_textbox).val(data.name);
  });

  socketio.on("modal_item_index_result", function(data){
    let old_index = data.old_index;
    let new_index = data.new_index;

    let tileID = $(".modal-here").attr("id_of_caller");
    if (tileID === data.tile_id) {
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

  socketio.on("modal_slider_result", function(data) {
    // update position
    let tileID = $(".modal-here").attr("id_of_caller");
    if (tileID === data.tile_id) {
      let triggerEvents = true; // or false
      let element = document.querySelector(".slider[data-id=" + data.id + "] input[type='range']");
      let slider_div = $(element).parent();
      slider_div.attr("data-prew-val", data.value);
      element.rangeSlider.update({
        value: data.value
      }, triggerEvents);
    }
  });

  socketio.on("modal_item_delete_result", function(data) {
    console.log(data.tile_id);
    console.log(data.index);

    let tileID = $(".modal-here").attr("id_of_caller");
    if (tileID === data.tile_id)
    {
      $($(".modal_items_edit_sortable .modal-edit-item")[data.index]).slideUp(function() {
        $(this).remove();
      });
    }

    // $(object).parent().parent().parent().slideUp(function() {
    //   $(object).parent().parent().parent().remove();
    // });
  });

  socketio.on("tile_delete_result", function(data){
    $(".tile[data-id="+data.tile_id+"]").parent().fadeOut(function() {$(this).remove()});
  });

  socketio.on("tile_icon_result", function(data){
    $(".tile[data-id="+data.tile_id+"] .tile-icon").attr("src",data.new_icon);
  });
  
  socketio.on("tile_type_result", function(data){
    let id_of_caller = $(".modal-here").attr("id_of_caller");
    if (data.tile_id === id_of_caller) {
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
    $(".tile[data-id='"+data.tile_id+"']").attr("data-id",data.new_id);
    $("#tile-mqtt-path").val("home/" + data.new_id);
    $(".modal-here").attr("id_of_caller", data.new_id);
  });

  socketio.on("modal_item_prepend_result", function(data) {
    let id_of_caller = $(".modal-here").attr("id_of_caller");
    if (data.tile_id === id_of_caller) {
      $(".modal_items_edit_sortable").prepend($(data.item));
      let item = $(".modal_items_edit_sortable").find(".modal-edit-item")[0];

      $(item).attr("id","modal_items_edit_sortable_last");
      $("#modal_items_edit_sortable_last").hide().slideDown().removeAttr("id");

      $(item).find(".modal-edit-item-dynamic-value").on("input",function(e){
        // ( > modal_edit_events.js )
        modalEditItemTextChanged(this);
      });
      $(item).find(".modal-edit-item-delete").on("click",function(e){
        modalEditItemDelete(this);
      });
    }
  });

  socketio.on("get_add_modal_result", function(data) {
    // ( > modal_init.js )
    initializeModal(data);
  });

  socketio.on("get_add_tile_result", function(data) {
    let selected_slide = $($(".swiper-slide")[data.slide_index]).find(".add_new_tile_element");
    $(data.tile_html).insertBefore(selected_slide).hide().fadeIn();
    let tile_array = $($(".swiper-slide")[data.slide_index]).find(".grid-square");
    let appended_tile = $(tile_array[tile_array.length-1]);
    $(appended_tile).each(function(){
      initializeHammerTile(this);
    });
  });

  

  socketio.on("get_modal_result", function(data) {
    handleModalResponse(data);
  });

  socketio.on("get_edit_modal_result", function(data) {
    console.log("Received edit modal");
    handleModalResponse(data);
  });

  socketio.on("get_settings_modal_result", function(data) {
      
    // ( > events.js )
    displaySettingsModal(data);
    $(".modal-edit-select-bcg").each(function() {
      let attr = $(this).attr('checked');
      if (typeof attr !== typeof undefined && attr !== false) {
        if ($("body").hasClass("dark")) {
          $(this).css({"border": "2px solid rgb(232, 93, 71)"});
        }
        else {
          $(this).css({"border": "2px solid rgb(23, 162, 184)"});
        }
      }
      Hammer(this).on("tap", function(elem) {
        // ( > modal_edit_events.js )
        modalEditPreviewImageTap(elem);
      });
    });
  });

  socketio.on("get_client_list_modal_result", function(data) {
    // ( > events.js )
    displaySettingsModal(data);
  });

  socketio.on("get_user_list_modal_result", function(data) {
    // ( > events.js )
    displaySettingsModal(data);
  });

  socketio.on("get_android_modal_result", function(data) {
    $(".modal-android").empty().append(data.modal);
    $("#my-android-modal").modal({ keyboard: true })
  });

  socketio.on("slide_index_result", function() {
    $(".swipe-body").attr("data-index-change", "true");
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
    swiper.appendSlide(data.slide);

    let isEditActive = $("body").attr("data-is-edit-active");

    let lastSlide = $($(".swiper-slide")[$(".swiper-slide").length-1])

    
    lastSlide.find(".tile").each(function(){
      initializeHammerTile(this);
    });

    // if (isEditActive === "true") {
    //   $(".add_new_tile_element").hide().fadeIn(2000);
    //   $(".exit-edit-mode-button").hide().fadeIn(2000);

    //   // Připnutí Hammer pro každé "+" tlačítko
    //   $(".swiper-slide-active .add_new_tile_element").each(function() {
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

      lastSlide.find(".swipe-header-textbox").each(function() {
        $( this ).prop("readonly",false)
        // $( this ).css({"border-bottom-width":"1px","border-bottom-style":"solid","width":"fit-content"});
      });

      $(".exit-edit-mode-button").hide().fadeIn(2000);

      let lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
      bindSortable(SortableTiles.length,lastSortablePage[lastSortablePage.length-1]);
    // }
  });

  socketio.on("slide_append_animation_result", function() {
    swiper.slideTo(swiper.slides.length, 1000);
  });

  socketio.on("slide_prepend_result", function(data) {
    swiper.prependSlide(data.slide);

    let isEditActive = $("body").attr("data-is-edit-active");

    if (isEditActive === "true") {
      $(".add_new_tile_element").hide().fadeIn(2000);
      $(".exit-edit-mode-button").hide().fadeIn(2000);

      // Připnutí Hammer pro každé "+" tlačítko
      $(".swiper-slide-active .add_new_tile_element").each(function() {
        let hammer = new Hammer(this);
        hammer.on("tap", function(el) {
          addNewTile();
        });
      });

      let lastSortablePage = document.getElementsByClassName("c_sortable_page_grid");
      bindSortable(SortableTiles.length,lastSortablePage[lastSortablePage.length-1]);
    }
  });

  socketio.on("slide_prepend_animation_result", function() {
    swiper.slideTo(0, 1000);
  });

  // Asynchronous communication for tile
  socketio.on("tile_value_result", function(data) {
    // Test each tile on the page
    let tileID = data.tile_id;
    let tileElement = $(".tile[data-id="+tileID+"]");
    let tileType = tileElement.attr("data-type");

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
    // Tile type is percentage
    else if (tileType === "value") {
      tileElement.find(".tile-value-value").text(data.value.value);
      tileElement.find(".tile-value-suffix").text(data.value.suffix);
    }
    else if (tileType === "value_double") {
      tileElement.find(".tile-value-left").text(data.value.left.value);
      tileElement.find(".tile-value-right").text(data.value.right.value);
      tileElement.find(".tile-suffix-left").text(data.value.left.suffix);
      tileElement.find(".tile-suffix-right").text(data.value.right.suffix);
    }
    else if (tileType === "alarm_clock") {
      // console.log(data.value);
      // console.log(data.value.main);
      // console.log(data.value.tuesday);


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
      console.log(tileId);

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
        console.log("tile active");
      }
      else {
        tileElement.toggleClass("tile-active",false);
        console.log("tile not active");
      }
      
      let tileDay = "Mon"
      if (tileMon === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Tue"
      if (tileTue === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Wed"
      if (tileWed === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Thu"
      if (tileThu === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Fri"
      if (tileFri === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Sat"
      if (tileSat === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false);
      tileDay = "Sun"
      if (tileSun === true) tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",true);
      else tileElement.find(".alarm-clock-glyph[data-type="+tileDay+"]").toggleClass("alarm-clock-glyph-active",false); 
    }
  });

  // Asynchronous communication for modal toggle
  socketio.on("modal_toggle_result", function(data) {
    console.log("ahoj jsoem tu");
    console.log(data);
    let tileID = $(".modal-here").attr("id_of_caller");

    // If tile ID is same
    if (tileID === data.tile_id) {
      $(".modal-toggle").each(function(){
        let toggleID = $(this).attr("data-id");

        // If toggle ID is same
        if (toggleID === data.id) {
          $(this).children().children().prop('checked', parseInt(data.value));
        }
      });
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

  // Reload page
  socketio.on("reload", function() {
    console.log("Server command: reload");
    location.reload();
  });

  socketio.on("connect", function() {
    console.log("Client connected to server");
    $(".server-status").text(_("Online"));
  });
    let ping_pong_times = [];
    let start_time;

    window.setInterval(function() {
        start_time = (new Date).getTime();
        socketio.emit("my-ping");
    }, 20000);

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
      $(".server-status").text(Math.round(sum / ping_pong_times.length) + " ms");
    });
  socketio.on("disconnect", function() {
    console.log("Client disconnected from server");
    $(".server-status").text(_("Offline"));

    if ($("body").attr("data-is-edit-active") === "true") {
      $(".bcg-normal").css({"opacity": 0, "transition": "0s all"});
      $(".bcg-edit").css({"opacity": 0.5, "transition": "0.5s all"});
    }
    else {
      $(".bcg-normal").css({"opacity": 0.4});
    }
    // $.notify({
    //   title: "<strong>Server</strong>",
    //   message: _("Server is now offline")
    // }, {
    //   type: "danger",
    //   delay: 0,
    //   mouse_over: "pause",
    //   allow_dismiss: true,
    //   placement: {
	// 	from: "top",
	// 	align: "center"
	//   },
    //   animate: {
    //     enter: "animated fadeInDown", //Down",
    //     exit: "animated fadeOutUp" //Up"
    //   },
    //   z_index: 2000
    // });
  });

  socketio.on("reconnect", function() {
    console.log("Server reconnected! Reloading...");

    setTimeout(() => {
      location.reload();
    }, 500);
  });

  // Asynchronous communication for global notifications
  socketio.on("notify", function(msg) {
    $.notify({
      title: "<strong>" + msg.title +  "</strong>",
      message: msg.message
    }, {
      type: msg.type,
      delay: 5000,
      mouse_over: "pause",
      allow_dismiss: true,
      /*placement: {
		from: "top",
		align: "center"
	  },*/
      animate: {
        enter: "animated fadeInRight", //Down",
        exit: "animated fadeOutRight" //Up"
      },
      z_index: 2000
    });
  });
});
