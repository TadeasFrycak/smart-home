// credits: <div>Icons made by <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"             title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


$(document).ready(function(){      
// Spustí se při načtení stránky

    console.log("+----------------------------------+");
    console.log("|     IoT Project, version 5.5     |");
    console.log("|     Last modified: 18.8.2019     |");
    console.log("|                                  |");
    console.log("|              © 2019              |");
    console.log("+----------------------------------+");

    // Asynchroní přijem dat
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('newstate', function(msg) {
        console.log("Received message: ");
        console.log(msg.mac);     
    });
    
    // Initializace Swiperu 
    var swiper = new Swiper('.swiper-container', {
        pagination: { el: '.swiper-pagination', },
        threshold: '10'
      });

    // Vypocet pozice pro scroll objekty
    var PredchoziProcenta = 0;    
    var overlayYpos = 210;
    
    $(document).on('input', '.slider', function() {                     // Spustí se při kliknutí nebo posunutím scroll modulu
        var output = $(this).val();                                     // Načítá okamžitou hodnotu kurzoru
        var konstanta = parseFloat(0.47619);                            // Konstanta pro přepočítávání pozice na pixely

        var procenta = Math.round(output * konstanta / 10) * 10;        // Počítání procent 
        var outputText = "";

        
        if (procenta == 0)  outputText = "OFF";                         // Rozhodování mezi stavem OFF nebo číselnou hodnotou
        else outputText = procenta + "%"; 
        
        overlayYpos = Math.abs((output - 210));                         // Počítání relatvní pozice pro .box (overlay)
        $('.debug').html(output - 210);
        
        if (procenta != PredchoziProcenta){
            console.log("released!");
            if (procenta == 0){
                $(this).parent().children('.item-image').fadeTo("slow",0.33);
                $(this).parent().children('.item-header').fadeTo("slow",0.33);
            }
            else{
                $(this).parent().children('.item-image').fadeTo("fast",1);
                $(this).parent().children('.item-header').fadeTo("fast",1);
            }
            PredchoziProcenta = procenta;
            
            $(this).parent().children().find("value").text(procenta);
            var Data_of_element = $(this).parent().children().find("module").html();
            
            $.post( "/post", {
                    data: Data_of_element
            });
            //$.get('/html_json', function(data) {
            //    console.log($.parseJSON(data));
            //});
            }

        if (procenta == 0) overlayYpos = 210;
        if (procenta == 100) overlayYpos = 0;
        
        $(this).parent().children(".item-status").text(outputText);
        $(this).parent().children(".box").css("top",overlayYpos + "px");
    });


    /*  -- Generování modulů -- */
    
    var device_config_array;
    var icons_array = null;
    
    // Načítání souborů 
    $.get('/static/device-config.txt', function(device_config_data) {
        $.get('/static/items.html.txt', function(items_data){
            $.get('/get_icons', function(data) {
                
                var current_page = 0;

                // Generuje pole z konfiguračních složek
                device_config_array = device_config_data.split('\n');
                items_data_list = items_data.split('\n');
                icons_array = $.parseJSON(data).icons;

                // Pro každý item zvlášť
                jQuery.each( device_config_array, function( i, val ) {
                    
                    var is_line_commented = device_config_array[i].indexOf(";"); // -1 = is not commented

                    if (device_config_array[i].indexOf("<page>") >= 0 && is_line_commented == -1)
                    {
                        current_page++;
                        var item_index = items_data_list.indexOf("<type='page'>") + 1;
                        var prepared_item = items_data_list[item_index];

                        var name = $.trim(device_config_array[i].split("<name>")[1].split("</name>")[0]);
                        prepared_item = prepared_item.replace("INSERT_HEADER", name);
                        prepared_item = prepared_item.replace("INSERT_ID","p" + current_page);
                        swiper.appendSlide([prepared_item]);

                        console.log("page added, " + name + " on page: " + current_page);
                    }
                    
                    if(device_config_array[i].indexOf("<module>") >= 0 && device_config_array[i].indexOf("</module") >= 0 && is_line_commented == -1)
                    {
                         var type = $.trim(device_config_array[i].split("<type>")[1].split("</type")[0]);
                         var name = $.trim(device_config_array[i].split("<name>")[1].split("</name>")[0]);
                         //var pageForItem = $.trim(device_config_array[i].split("<page-id>")[1].split("</page-id>")[0]);
                         var iconID = $.trim(device_config_array[i].split("<icon-id>")[1].split("</icon-id>")[0]);

                         var icon_prepare = "icon" + iconID;
                                         
                        // Generuje toggle item
                        if (type == "toggle") 
                        {
                            var item_index = items_data_list.indexOf("<type='toggle'>") + 1;
                            var prepared_item = items_data_list[item_index];
                            
                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
                            console.log("Try to: " + current_page);
                            //$("#p" + current_page).append("<div class='item item-toggle selectDisable'><img src='INSERT_IMAGE' class='item-image' style='opacity:0.33;'><div class='item-header'style='opacity:0.33;'>INSERT_HEADER</div><div class='item-status'>OFF</div><div class='item-info' style='display:none;>INSERT_INFO</div></div>")
                            //$("#p1").append(prepared_item);
                            $("#p" + current_page).append(prepared_item);  
                            swiper.update();
                        }
                        

                        // Generuje scroll item
                        if (type == "scroll") 
                        {
                            var item_index = items_data_list.indexOf("<type='scroll'>") + 1;
                            var prepared_item = items_data_list[item_index];

                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
                            console.log("stranka: " + current_page);
                            $("#p" + current_page).append(prepared_item);  
                            swiper.update();
                        } 
                        
                        
                    }

                    if (device_config_array[i].indexOf("<spacer>") >= 0 && is_line_commented == -1)
                    {
                        var item_index = items_data_list.indexOf("<type='spacer'>") + 1;
                        //$("#" + current_page).append(items_data_list[item_index]);
                    }


                });

            }, 'text');
        }, 'text');
     }, 'text');

     
     
     // Definování CSS barev do proměnných
     var item_unactive_color = 'rgb(206, 206, 206)';
     var item_active_color = 'rgb(255, 255, 255)';


    /*  -- Načítání pbrázků na pozadí -- */

    $.get('/get_background_images', function(data) {
        $('body').css('background-image', 'url("' + $.parseJSON(data).random_image + '")');
    });
     

    /*  -- Detekování stisku toggle itemu -- */

    $('body').on('click', '.item-toggle', function() {

        var value = 0;

        if($(this).css('background-color')==item_unactive_color)
        {
            ChangeItemState(this,100);
            value = 100;
        }
        else if($(this).css('background-color')==item_active_color)
        {
            ChangeItemState(this,0);
            value = 0;
        }
        
        $(this).find("value").text(value);
        
        var Data_of_element = $(this).find("module").html();
        
        //$.post( "/post", {
             //       data: "x"
            //});
        //$.get('/html_json', function(data) {
        //    console.log($.parseJSON(data));
        //});
        
    });


    function ChangeItemState(button, stav){


        if(stav == 100)
        {
            $(button).css('background-color', item_active_color);
            $(button).children('.item-status').text("ON");
            $(button).children('.item-image').fadeTo("fast",1);
            $(button).children('.item-header').fadeTo("fast",1);
        }
        else if (stav == 0){
            $(button).css('background-color', item_unactive_color);
            $(button).children('.item-status').text("OFF");
            $(button).children('.item-image').fadeTo("slow",0.33);
            $(button).children('.item-header').fadeTo("slow",0.33);

        }
    }


    function toggleButton(id,stav){
        $( "body .item-info id" ).each(function( index ) {

            if ($( this ).html() == id){console.log("found: " + id); 
            var itemToToggle = $( this ).parent().parent().parent();
            
            ChangeItemState(itemToToggle,stav);
        }
        });
    }

  });

  