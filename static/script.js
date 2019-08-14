// credits: <div>Icons made by <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"             title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


$(document).ready(function(){      
// Spustí se při načtení stránky
    // Asynchroní přijem dat
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('newstate', function(msg) {
        console.log("Received msg: " + msg.mac);    
    });
    
    // Initializace Swiperu 
    var swiper = new Swiper('.swiper-container', {
        pagination: {
          el: '.swiper-pagination',
        },
        threshold: '10'
      });

    var PredchoziProcenta = 0;    
    var overlayYpos = 210;
    
    $(document).on('input', '.slider', function() {     
    //$( ".slider" ).on( "click", function() {            // Spustí se při kliknutí nebo posunutím scroll modulu
    //$(".slider").on("click"),function(
        
        var output = $(this).val();                                     // Načítá hodnotu scroll modulu 
        //var konstanta = parseFloat(0.476190476190476); 
        var konstanta = parseFloat(0.47619);                            // Konstanta pro přepočítávání pozice

        var procenta = Math.round(output * konstanta / 10) * 10;        // Počítání procent 
        var outputText = "";

        
        if (procenta == 0)  outputText = "OFF";                         // Rozhodování mezi stavem OFF nebo číselnou hodnotou
        else outputText = procenta + "%"; 
        
        overlayYpos = Math.abs((output - 210));                     // Počítání relatvní pozice pro .box (overlay)
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
                        
                        var type = device_config_array[i].substring(device_config_array[i].indexOf("<type>") + 6,device_config_array[i].indexOf("</type>"));
                        var name = device_config_array[i].substring(device_config_array[i].indexOf("<name>") + 6,device_config_array[i].indexOf("</name>"));
                        var pageForItem = device_config_array[i].substring(device_config_array[i].indexOf("<page-id>") + 9,device_config_array[i].indexOf("</page-id>"));
                        var iconID = device_config_array[i].substring(device_config_array[i].indexOf("<icon-id>") + 9,device_config_array[i].indexOf("</icon-id>")); 

                        // Generuje item příslušného typu na příslušnou stránku
                        if (type == "toggle") 
                        {
                            var prepared_item = items_data_list[1];
                            prepared_item = prepared_item.replace("<div class='item-header'style='opacity:0.33;'></div>", "<div class='item-header'style='opacity:0.33;'>" + name + "</div>");
                            prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + String(device_config_array[i]) + "</div>");
                            prepared_item = prepared_item.replace("<img src=''", "<img src='" + icons_array[iconID] + "'");
                            $("#" + pageForItem).append(prepared_item);  
                        }

                        // Generuje item příslušného typu na příslušnou stránku
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

     
     
     
     var item_unactive_color = 'rgb(206, 206, 206)';
     var item_active_color = 'rgb(255, 255, 255)';

     $.get('/static/wallpapers-paths.txt', function(wallpapers) {
        wallpper_array = wallpapers.split('\n');
        var wallpaper_index = Math.floor(Math.random() * wallpper_array.length) + 1
        console.log(wallpper_array[wallpaper_index]);

        $('body').css('background-image', 'url("' + wallpper_array[wallpaper_index] + '")');
     },'text');
     
     

    // switch(Math.floor(Math.random() * 8) + 1){
    //     case 1:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg1.dms")');
    //         break;
    //     case 2:
    //             $('body').css('background-image', 'url("/static/Img/bckImg2.jpg")');
    //         break;
    //     case 3:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg4.jpg")');
    //         break;
    //     case 4:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg5.jpg")');
    //         break;
    //     case 5:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg6.jpg")');
    //         break;
    //     case 6:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg7.jpg")');
    //         break;
    //     case 7:
    //             $('body').css('background-image', 'url("/static/Img/bcgImg8.jpg")');
    //         break;
    //     case 8:
    //         $('body').css('background-image', 'url("/static/Img/bcgImg9.jpg")');
    //     break;
    // }


    $('body').on('click', '.item-toggle', function() {
        ChangeItemState(this,2); // DRUHY CISLO MUSI BYT 2 VZDYCKY POKUD NECHCEEM NIC KONKRETNIHO!!!

        // JEN PRO TEST! NASTAVUJI OD KTERE SE MA ZAPNOUT
        //toggleButton(3,1);
        
    });


    function ChangeItemState(button, stav){
        if(stav == 1 || stav == 2 && $(button).css('background-color')==item_unactive_color)
        {
            //console.log(button);
            $(button).css('background-color', item_active_color);
            $(button).children('.item-status').text("ON");
            $(button).children('.item-image').fadeTo("fast",1);
            $(button).children('.item-header').fadeTo("fast",1);
        }
        else if (stav == 0 || stav == 2 && $(button).css('background-color')==item_active_color){
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

  