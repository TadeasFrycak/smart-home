// credits: <div>Icons made by <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"             title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


$(document).ready(function(){      
// Spustí se při načtení stránky

    console.log("+----------------------------------+");
    console.log("|     IoT Project, version 5.6     |");
    console.log("|     Last modified: 20.8.2019     |");
    console.log("|                                  |");
    console.log("|              © 2019              |");
    console.log("+----------------------------------+");

    // vytviří radiální ukazatel

    var GaugesByID = [];
    var GaugesNumber = 0;
    function createRadGauge(t,e,a,n){function r(t,e,a,n){return{x:t+a*Math.cos(n),y:e+a*Math.sin(n)}}function s(t,e,a,n,s,o){var d=r(t,e,a,-Math.PI),l=r(t,e,a,-Math.PI*(1-1/(o-s)*(n-s))),i=["M",d.x,d.y,"A",a,a,0,0,1,l.x,l.y].join(" ");return i}var o='<svg class="rGauge" viewBox="0 0 200 145"><path class="rGauge-base" id="'+t+'_base" stroke-width="30" /><path class="rGauge-progress" id="'+t+'_progress" stroke-width="30" stroke="#1565c0" /><text class="rGauge-val" id="'+t+'_val" x="100" y="105" text-anchor="middle"></text><text class="rGauge-min-val" id="'+t+'_minVal" x="40" y="125" text-anchor="middle"></text><text class="rGauge-max-val" id="'+t+'_maxVal" x="160" y="125" text-anchor="middle"></text></svg>';document.getElementById(t).innerHTML=o,document.getElementById(t+"_base").setAttribute("d",s(100,100,60,1,0,1)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,e,e,a)),document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var d={setVal:function(r){return r=Math.max(e,Math.min(r,a)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,r,e,a)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),d},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("stroke",e),d}};return d}function createVerGauge(t,e,a,n){var r='<svg class="vGauge" viewBox="0 0 145 145"><rect class="vGauge-base" id="'+t+'_base" x="30" y="25" width="30" height="100"></rect><rect class="vGauge-progress" id="'+t+'_progress" x="30" y="25" width="30" height="0" fill="#1565c0"></rect><text class="vGauge-val" id="'+t+'_val" x="70" y="80" text-anchor="start"></text><text class="vGauge-min-val" id="'+t+'_minVal" x="70" y="125"></text><text class="vGauge-max-val" id="'+t+'_maxVal" x="70" y="30" text-anchor="start"></text></svg>';document.getElementById(t).innerHTML=r,document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var s={setVal:function(r){r=Math.max(e,Math.min(r,a));var o=100/(a-e)*(r-e);return document.getElementById(t+"_progress").setAttribute("height",o),document.getElementById(t+"_progress").setAttribute("y",25+(100-o)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),s},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("fill",e),s}};return s}
    
    
    function sleep(milliseconds) {
      var start = new Date().getTime();
      for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
          break;
        }
      }
    }
    
    // Asynchroní přijem dat
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('newstate', function(msg) {
        //console.log("Received message: ");
        console.log(msg.type);     
        
        if (msg.type="console")
        {
            if (msg.status=="log")
            {
                console.log(msg.message);
            }
            
            else if (msg.status=="warning")
            {
                console.warning(msg.message);
            }
            
            else if (msg.status=="error")
            {
                console.log(msg.message);
            }
        }
        
        else if (msg.type="temperature_sensor")
        {
            var before_value = parseInt($("#" + msg.id).parent().parent().children().find("value").html());
            GaugesByID[msg.id].setVal(parseInt(msg.value)).setColor(msg.color);
            $("#" + msg.id).parent().parent().children().find("value").html(msg.value);
        }
        
        
    });
    
    // Initializace Swiperu 
    var swiper = new Swiper('.swiper-container', {
        pagination: { el: '.swiper-pagination', },
        threshold: '10'
      });

    


    // Vypocet pozice pro scroll objekty
    var PredchoziProcenta = 0;    
    var overlayYpos = 210;

    $(document).on('input', '.rgb-slider', function(e) {  

        var target = $(e.target);

        var output = $(this).val();      
        $(this).parent().children(".rgb-slider-blanket").css("top",150 - output + "px");

        var hodnota = Math.round(output /1.5);
        var name_of_color = $(this).parent().parent().children(".rgb-label").html().toLowerCase();

        var Data_of_element = $(this).parent().parent().parent().parent().find("module").html();

        $(this).parent().parent().parent().parent().find(name_of_color).text(hodnota);


        //console.log(Data_of_element);
        $.post( "/post", {
                data: Data_of_element
        });
        //$.get('/html_json', function(data) {
        //        console.log($.parseJSON(data));
        //});



    });

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
                    }
                    
                    if(device_config_array[i].indexOf("<module>") >= 0 && device_config_array[i].indexOf("</module") >= 0 && is_line_commented == -1)
                    {
                         var type = $.trim(device_config_array[i].split("<type>")[1].split("</type")[0]);
                         var name = $.trim(device_config_array[i].split("<name>")[1].split("</name>")[0]);
                         
                         //var pageForItem = $.trim(device_config_array[i].split("<page-id>")[1].split("</page-id>")[0]);
                         var iconID = $.trim(device_config_array[i].split("<icon-id>")[1].split("</icon-id>")[0]);

                         var icon_prepare = "icon" + iconID;
                        
                        // Generuje gauge item
                        if (type == "gauge") 
                        {

                            var id = $.trim(device_config_array[i].split("<id>")[1].split("</id>")[0]);
                            var value_from = $.trim(device_config_array[i].split("<value-from>")[1].split("</value-from>")[0]);
                            var value_to = $.trim(device_config_array[i].split("<value-to>")[1].split("</value-to>")[0]);
                            var end_char = $.trim(device_config_array[i].split("<end-char>")[1].split("</end-char>")[0]);
                            var gauge_color = $.trim(device_config_array[i].split("<gauge-color>")[1].split("</gauge-color>")[0]);
                            var value = $.trim(device_config_array[i].split("<value>")[1].split("</value>")[0]);

                            var item_index = items_data_list.indexOf("<type='gauge'>") + 1;
                            var prepared_item = items_data_list[item_index];
                            
                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
                            prepared_item = prepared_item.replace("INSERT_ID", id);

                            $("#p" + current_page).append(prepared_item);  
                            GaugesByID[id] = createRadGauge(id,value_from,value_to,end_char).setVal(value).setColor(gauge_color);
                            
                            GaugesNumber++;
                            swiper.update();
                        }

                        if (type == "rgb_slider") 
                        {
                            var item_index = items_data_list.indexOf("<type='rgb_slider'>") + 1;
                            var prepared_item = items_data_list[item_index];
                            
                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
                            $("#p" + current_page).append(prepared_item);  
                            swiper.update();
                        }

                        if (type == "rgbw_slider") 
                        {
                            var item_index = items_data_list.indexOf("<type='rgbw_slider'>") + 1;
                            var prepared_item = items_data_list[item_index];
                            
                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
                            $("#p" + current_page).append(prepared_item);  
                            swiper.update();
                        }

                        // Generuje toggle item
                        if (type == "toggle") 
                        {
                            var item_index = items_data_list.indexOf("<type='toggle'>") + 1;
                            var prepared_item = items_data_list[item_index];
                            
                            prepared_item = prepared_item.replace("INSERT_HEADER", name);
                            prepared_item = prepared_item.replace("INSERT_INFO", device_config_array[i]);
                            prepared_item = prepared_item.replace("INSERT_IMAGE", icons_array[icon_prepare]);
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
                            $("#p" + current_page).append(prepared_item);  
                            swiper.update();
                        } 
                        
                        
                    }

                    if (device_config_array[i].indexOf("<spacer>") >= 0 && is_line_commented == -1)
                    {
                        var item_index = items_data_list.indexOf("<type='spacer'>") + 1;
                        $("#" + current_page).append(items_data_list[item_index]);
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

    $('body').on('click', '.item-toggle', function(e) {

        var target = $(e.target);

        if(!target.is('.rgb-slider')) {

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
            $.post( "/post", {
                    data: Data_of_element
            });
            $.get('/html_json', function(data) {
                console.log($.parseJSON(data));
            });

         }

        
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

  