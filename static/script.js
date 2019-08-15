// credits: <div>Icons made by <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"             title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


$(document).ready(function(){      
// Spustí se při načtení stránky

    console.log("+----------------------------------+");
    console.log("|     IoT Project, version 5.4     |");
    console.log("|     Last modified: 15.8.2019     |");
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
            
            if (procenta == 0){
                $(this).parent().children('.item-image').fadeTo("slow",0.33);
                $(this).parent().children('.item-header').fadeTo("slow",0.33);
            }
            else{
                $(this).parent().children('.item-image').fadeTo("fast",1);
                $(this).parent().children('.item-header').fadeTo("fast",1);
            }
            PredchoziProcenta = procenta;
        }

        if (procenta == 0) overlayYpos = 210;
        if (procenta == 100) overlayYpos = 0;
        
        $(this).parent().children(".item-status").text(outputText);
        $(this).parent().children(".box").css("top",overlayYpos + "px");
    });



    /*  -- Generování modulů -- */
    
    var device_config_array;

    // Načítání souborů 
    $.get('/static/device-config.txt', function(device_config_data) {
        $.get('/static/items.html.txt', function(items_data){
            $.get('/static/icons-path.txt', function(icons_path_file) {

                // Generuje pole z konfiguračních složek
                device_config_array = device_config_data.split('\n');
                items_data_list = items_data.split('\n');
                icons_array = icons_path_file.split('\n');

                // Pro každý item zvlášť
                jQuery.each( device_config_array, function( i, val ) {

                    if(device_config_array[i].indexOf("<module>") >= 0 && device_config_array[i].indexOf("</module") >= 0 && device_config_array[i].indexOf(";") == -1)
                    {
                        
                        var type = $.trim(device_config_array[i].split("<type>")[1].split("</type")[0]);;
                        var name = $.trim(device_config_array[i].split("<name>")[1].split("</name>")[0]);
                        var pageForItem = $.trim(device_config_array[i].split("<page-id>")[1].split("</page-id>")[0]);
                        var iconID = $.trim(device_config_array[i].split("<icon-id>")[1].split("</icon-id>")[0]);

                        // Generuje toggle item
                        if (type == "toggle") 
                        {
                            var prepared_item = items_data_list[1];
                            prepared_item = prepared_item.replace("<div class='item-header'style='opacity:0.33;'></div>", "<div class='item-header'style='opacity:0.33;'>" + name + "</div>");
                            prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + String(device_config_array[i]) + "</div>");
                            prepared_item = prepared_item.replace("<img src=''", "<img src='" + icons_array[iconID] + "'");
                            $("#" + pageForItem).append(prepared_item);  
                        }

                        // Generuje scroll item
                        if (type == "scroll") 
                        {
                            var prepared_item = items_data_list[3];
                            prepared_item = prepared_item.replace("<div class='item-header'></div>", "<div class='item-header'style='opacity:0.33;'>" + name + "</div>");
                            prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + device_config_array[i] + "</div>");
                            prepared_item = prepared_item.replace("<img src=''", "<img src='" + icons_array[iconID] + "'");
                            $("#" + pageForItem).append(prepared_item);  
                        }   
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
        var wallpper_array = $.parseJSON(data).images;
        console.log($.parseJSON(data));
        console.log(wallpper_array);
        var wallpaper_index = Math.floor(Math.random() * wallpper_array.length)

        $('body').css('background-image', 'url("' + wallpper_array[wallpaper_index] + '")');
    });
     

    /*  -- Detekování stisku toggle itemu -- */

    $('body').on('click', '.item-toggle', function() {
        //ChangeItemState(this,2); // DRUHY CISLO MUSI BYT 2 VZDYCKY POKUD NECHCEEM NIC KONKRETNIHO!!!

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

        $(this).animate({
            "color": "#ffffff"
        }, 1500);

        

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        var Data_of_element = $(this).find("module").html();
        Jasonify = Data_of_element.split(' ');
        //console.log(Jasonify);
        Jasonify.forEach(function(entry) {
            if (entry != ""){
                entry = entry.replace("<","\"")
                console.log(entry);
            }
        });
        
        var element = Data_of_element;
        //console.log(element);
        //  This gives you a string representing that element and its content
        var html = element.oute; 
        //console.log(html);      
        //  This gives you a JSON object that you can send with jQuery.ajax's `data`
        // option, you can rename the property to whatever you want.
        var data = { html: html }; 

        //  This gives you a string in JSON syntax of the object above that you can 
        // send with XMLHttpRequest.
        var json = JSON.stringify(data);

        //console.log(json);
        
        $.get('/change_item_state/{"item_id":' + "ID_of_element" + ', "value":' + "value" + '}', function(data) {
            //console.log("Sending data, synchronized..");
            //console.log("Response: " + $.parseJSON(data));
            //  This gives you an HTMLElement object


            //console.log($.parseJSON(data))
        });

        // JEN PRO TEST! NASTAVUJI OD KTERE SE MA ZAPNOUT
        //toggleButton(3,1);
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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

  