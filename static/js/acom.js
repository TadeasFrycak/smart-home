$(document).ready(function(){
  // ----------------------------------------------
  // Receive asynchronous communication
  // ----------------------------------------------

  // Initialise communication
  socketio = io("/com");

  socketio.on("user_change_mode_result", function(data) {
    if (data.mode === "light") {
      $("body").removeClass("dark").addClass("light");
      $(".add-img").attr("src","img/static/add.png");
      $(".page_settings_icon").attr("src","img/static/settings.png");
    }
    else if (data.mode === "dark") {
      $("body").removeClass("light").addClass("dark");
      $(".add-img").attr("src","img/static/add-dark.png");
      $(".page_settings_icon").attr("src","img/static/settings-dark.png");
    }
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
    if (data.tile_values) {
      $(".tile-values-wrapper").empty().append(data.tile_values);
    }

    $(".tile[data-id="+data.tile_id+"]").parent().replaceWith(data.tile_html);
    $(".tile[data-id="+data.tile_id+"]").each(function(){
      initializeHammerTile(this);
    });

    initImages();
    
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

  socketio.on("add_modal_item_result", function(data) {
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
    $(data.tile_html).insertBefore(selected_slide);
    $(data.tile_html).each(function(){
      console.log(this);
      initializeHammerTile(this);
    });
  });

  

  socketio.on("get_modal_result", function(data) {
    handleModalResponse(data);
  });

  socketio.on("get_edit_modal_result", function(data) {
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

    let isEditActive = $("body").attr("is_edit_active");

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

  socketio.on("slide_append_animation_result", function() {
    swiper.slideTo(swiper.slides.length, 1000);
  });

  socketio.on("slide_prepend_result", function(data) {
    swiper.prependSlide(data.slide);

    let isEditActive = $("body").attr("is_edit_active");

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

  socketio.on("slide_index_result", function(data) {
    if (data.new_index > data.old_index) {
      // TODO když je uživatel na new_index tak ho přesuň na index na ktereje se tato page přesune
      // TODO FILIPE tuhle funkci (měnění indexů věcí) bys mohl zdynamičnit, používá se často, dej ji do jedné funkce
      let all_slides_within_slide = $("body").find(".swiper-slide");
      let selected_slide_old = all_slides_within_slide[data.old_index];
      let selected_slide_new;

      let temporary_slide_old = $(selected_slide_old).clone();

      $(selected_slide_old).remove();

      if (data.new_index === all_slides_within_slide.length) {
        selected_slide_new = all_slides_within_slide[data.new_index-1];
        $(temporary_slide_old).insertAfter($(selected_slide_new));
      }
      else {
        selected_slide_new = all_slides_within_slide[data.new_index];
        if (data.new_index > data.old_index) $(temporary_slide_old).insertAfter($(selected_slide_new));
        if (data.new_index < data.old_index) $(temporary_slide_old).insertBefore($(selected_slide_new));
      }
    }

    else if (data.new_index < data.old_index) {
      // TODO když je uživatel na new_index tak ho přesuň na index na ktereje se tato page přesune
      let all_slides_within_slide = $("body").find(".swiper-slide");
      let selected_slide_old = all_slides_within_slide[data.old_index];
      let selected_slide_new;

      let temporary_slide_old = $(selected_slide_old).clone();

      $(selected_slide_old).remove();
      // TODO FILIPE tuhle funkci (měnění indexů věcí) bys mohl zdynamičnit, používá se často, dej ji do jedné funkce
      if (data.new_index === all_slides_within_slide.length) {
        selected_slide_new = all_slides_within_slide[data.new_index-1];
        $(temporary_slide_old).insertAfter($(selected_slide_new));
      }
      else {
        selected_slide_new = all_slides_within_slide[data.new_index];
        if (data.new_index > data.old_index) $(temporary_slide_old).insertAfter($(selected_slide_new));
        if (data.new_index < data.old_index) $(temporary_slide_old).insertBefore($(selected_slide_new));
      }
    }
    if (swiper.realIndex === data.old_index) {
      swiper.slideTo(data.new_index, 1000);
    }

  });

  // Asynchronous communication for tile
  socketio.on("tile_value_result", function(data) {
    // Test each tile on the page
    $(".tile").each(function() {
      let tileID = $(this).attr("data-id");

      // If tile ID is same
      if (tileID === data.id) {
        let tileType = $(this).attr("data-type");

        // Tile type is toggle
        if (tileType === "toggle") {
          let tileStateLast = $(this).find(".tile-status").text();
          let tileStateCurrent = data.value;

          // Turn tile off
          if (tileStateLast.toLowerCase() === "on" && tileStateCurrent === 0) {
            $(this).find(".tile-status").text("OFF"); $(this).toggleClass("tile-active");
            $(this).find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");
          }

          // Turn tile on
          else if (tileStateLast.toLowerCase() === "off" && tileStateCurrent === 1) {
            $(this).find(".tile-status").text("ON"); $(this).toggleClass("tile-active");
            $(this).find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
          }
        }

        // Tile type is percentage
        else if (tileType === "percentage") {
          $(this).find(".tile-input-value").text(data.value);
        }
      }
    });
  });

  // Asynchronous communication for modal toggle
  socketio.on("modal_toggle_result", function(data) {
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
    location.reload();
  });

  socketio.on("connect", function() {
    $(".server-status").text(_("Online"));
  });

  socketio.on("disconnect", function() {
    $(".server-status").text(_("Offline"));
  });

  socketio.on("reconnect", function() {
    location.reload();
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