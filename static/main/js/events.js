$(document).ready(function(){
    // ----------------------------------------------
    // Events
    // ----------------------------------------------
    // Settings icon

    $('.dropdown').on('show.bs.dropdown', function(e){
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });

    // ADD SLIDEUP ANIMATION TO DROPDOWN //
    $('.dropdown').on('hide.bs.dropdown', function(e){
        e.preventDefault();
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp(400, function(){
            //On Complete, we reset all active dropdown classes and attributes
            //This fixes the visual bug associated with the open class being removed too fast
            $('.dropdown').removeClass('show');
            $('.dropdown-menu').removeClass('show');
            $('.dropdown').find('.dropdown-toggle').attr('aria-expanded','false');
        });
    });

    function exit_edit_mode_fnct(){
        //$.notify({
        //        title: "<strong>Upravovací mód</strong>",
        //        message: "Upravovací  mód je deaktivovaný. Všechna nastavení byla uložena."
        //    }, {
        //        type: "info",
        //        delay: 2000,
        //        placement: {
        //            from: "top",
        //            align: "center"
        //        },
        //        mouse_over: "pause",
        //        allow_dismiss: true,
        //        animate: {
        //            enter: 'animated fadeInDown',
        //            exit: 'animated fadeOutUp'
        //        },
        //        z_index: 2000
        //    });
        is_edit = false;
        mySwiper.allowTouchMove = true;
        $(".tile_ghost_prefab_class").parent().fadeOut(2000);
        $(".btn_exit_edit_mode").show().fadeOut(2000);
        $(".bcg-image").fadeOut(2000);
        setTimeout(() => {$("#edit_page_dropdown").replaceWith("<a class='dropdown-item' id='edit_page_dropdown'>Upravit tuto stránku</a>");}, 300);
    }

    function hide_hexagon_dropdown()
    {
        for (i = 0; i < dropdowns.length; i++) { 
            dropdowns[i].hide();
          }
    }

    $('#myModal').on('hidden.bs.modal', function () {
        // do something…
        alert("aa");
    })


    $("body").on("click", ".modal_add_new_item", function(e){
        // Poslání + příjem okénka pro jednotlicé itemy
        $.post( "/get_modal_edit_item",
                {
                    "type": $(this).text()
                },

                function(result){
                    // modal_items_edit_sortable_last
                    var json = JSON.parse(result);
                    $(".modal_items_edit_sortable").prepend($(json.item));
                    var x_ = $(".modal_items_edit_sortable").find(".modal_items_edit_sortable_item")[0];
                    $(x_).attr('id','modal_items_edit_sortable_last');
                    $("#modal_items_edit_sortable_last").hide().slideDown();
                    $("#modal_items_edit_sortable_last").removeAttr('id');
                    });
    });

    $("body").on("click", ".modal_items_edit_sortable_item", function(e){
        if ($('.modal_items_edit_sortable_item_dropdown:hover').length == 0) {
            var status_display = $(this).find(".modal_items_edit_sortable_item_dropdown").css("display");
            if (status_display == "block") $(this).find(".modal_items_edit_sortable_item_dropdown").slideUp();
            if (status_display == "none") $(this).find(".modal_items_edit_sortable_item_dropdown").slideDown();
        }

    });

    

    $("body").on("click", ".modal_edit_dropdown_delete", function(e){
        console.log($(this).parent().parent().parent().closest(""));
        $(this).parent().parent().parent().slideUp();
    });
    

    $("body").on("click", "#edit_page_dropdown", function(e){
        hide_hexagon_dropdown();
        if (is_edit == true)
        {
            exit_edit_mode_fnct();
        }
        else if (is_edit == false)
        {
//            new Sortable(gridDemo, {
//        animation: 150,
//        ghostClass: 'blue-background-class'
//    });
            //$.notify({
            //    title: "<strong>Upravovací mód</strong>",
            //    message: "Upravovací  mód je aktivní"
            //}, {
            //    type: "info",
            //    delay: 2000,
            //    placement: {
            //        from: "top",
            //        align: "center"
            //    },
            //    mouse_over: "pause",
            //    allow_dismiss: true,
            //    animate: {
            //        enter: 'animated fadeInDown',
            //        exit: 'animated fadeOutUp'
            //    },
            //    z_index: 2000
            //});
            is_edit = true;
            mySwiper.allowTouchMove = false;
            $("#gridDemo").append("<div class='grid-square'><div class='tile tile_ghost_prefab_class' data-id='tile_ghost_prefab' data-type='toggle'><div class='tileTextLayer'><img src='::img_src::' class='tileImage'><span class='tileDescription'>Uprav mě!</span></div><div class='titeAtributes'>test</div><div class='tile_edit_prefab tileTouchLayer tileToggle tileModal'></div></div></div>");
            $(".swiper-slide").append("<button type='button' class='btn btn-danger btn_exit_edit_mode'>Ukončit upravovací mód</button>");
            $(".btn_exit_edit_mode").hide().fadeIn(2000);
            $(".tile_ghost_prefab_class").hide().fadeIn(2000);

            $('.tile_edit_prefab').each(function(){   //tagname based selector
                var mc = new Hammer(this);
                mc.on("tap", function() {   

                    return false;
                });
            });
            $(".bcg-image").fadeIn(2000);
            setTimeout(() => {$("#edit_page_dropdown").replaceWith("<a class='dropdown-item' id='edit_page_dropdown'>Ukončit upravovací mód</a>");}, 300);
            
        }  $(document.body);
    });

    $("body").on("click", ".btn_exit_edit_mode", function(e){
        exit_edit_mode_fnct();
        hide_hexagon_dropdown();
    });

    dropdowns = [];
    $(".page_settings_icon").each(function(){

    });

    $(document.body).on("click", "#collapse-items", function(e) {
        $(".modal_items_edit_sortable_item_dropdown").slideUp();
    });

    $(document.body).on("click", "#unpack-items", function(e) {
        $(".modal_items_edit_sortable_item_dropdown").slideDown();
        //$('#myModal').animate({ scrollTop: $(document).height() }, "slow");
    });

    $(document.body).on("click", "#scroll-up", function(e) {
            $('#myModal').animate({scrollTop: 0}, 'slow');
          });


    // Modal toggle button
    $("body").on("change", ".modal_toggle", function(e){
            var object_id = $(this).parent().parent().parent().attr("data-id");
            var object_state = "";
            e.stopPropagation();
            e.stopImmediatePropagation();

            // Checked
            if($(this).prop("checked") === true){
                object_state = "1";
            }

            // Unchecked
            else if($(this).prop("checked") === false){
                object_state = "0";
            }

            value = $("#myModal").data("id_of_caller");

            $.post("/toggle", {
                "i": object_id,
                "v": object_state,
                "id_tile": value
                },
                function(result){});    
            
        
    });








});
