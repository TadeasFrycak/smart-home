$(document).ready(function(){      // Spustí se při načtení stránky

    console.log("aaaaaaaa");

    //$(document).on('input', '.slider', function() {      
    //$('body').on('click', '.item-toggle', function() {   
    //$(".item" ).on('input', '.slider', function() {   
    $(document).on('input', '.slider', function() {     
    //$( ".slider" ).on( "click", function() {            // Spustí se při kliknutí nebo posunutím scroll modulu
    //$(".slider").on("click"),function(
        
        var output = $(this).val();                                     // Načítá hodnotu scroll modulu 
        var konstanta = parseFloat(0.476190476190476);                  // Konstanta pro přepočítávání pozice

        var procenta = Math.round(output * konstanta / 10) * 10;        // Počítání procent 
        var outputText = "";
        if (procenta == 0)  outputText = "OFF";                         // Rozhodování mezi stavem OFF nebo číselnou hodnotou
        else outputText = procenta + "%"; 

        var overlayYpos = Math.abs((output - 210));                     // Počítání relatvní pozice pro .box (overlay)
        $('.debug').html(output - 210);
        
        $(this).parent().children(".item-status").text(outputText);
        $(this).parent().children(".box").css("top",overlayYpos + "px");

        //console.log($(this).parent().children(".item-status").html());
        //$(document).find(".box").css("top",overlayYpos + "px");
        //$(document).find(".item-status").text(outputText);
        
       //$(this).closest(".overlay").append('<style>.overlay:before{top:'+overlayYpos+'px;}</style>');
       
    });






    var device_config_array;

    $.get('device-config.txt', function(device_config_data) {
        $.get('items.html.txt', function(items_data){

            device_config_array = device_config_data.split('\n');
            items_data_list = items_data.split('\n');
            //console.log(device_config_array);

            jQuery.each( device_config_array, function( i, val ) {


                if(device_config_array[i].indexOf("<module>") >= 0 && device_config_array[i].indexOf("</module") >= 0 && device_config_array[i].indexOf(";") == -1)
                {
                    
                    var type = device_config_array[i].substring(device_config_array[i].indexOf("<type>") + 6,device_config_array[i].indexOf("</type>"));
                    var name = device_config_array[i].substring(device_config_array[i].indexOf("<name>") + 6,device_config_array[i].indexOf("</name>"));

                    if (type == "toggle") 
                    {
                        var prepared_item = items_data_list[1];
                        prepared_item = prepared_item.replace("<div class='item-header'style='opacity:0.33;'></div>", "<div class='item-header'style='opacity:0.33;'>" + name + "</div>");

                        prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + device_config_array[i] + "</div>");
                        $("main").append(prepared_item);  
                    }

                    if (type == "scroll") 
                    {
                        var prepared_item = items_data_list[3];
                        prepared_item = prepared_item.replace("<div class='item-header'></div>", "<div class='item-header'>" + name + "</div>");
                        console.log(name);

                        prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + device_config_array[i] + "</div>");
                        $("main").append(prepared_item);  
                    }

                    
                }

            });


        }, 'text');
     }, 'text');

     

     



    var item_unactive_color = 'rgb(206, 206, 206)';
    var item_active_color = 'rgb(255, 255, 255)';


    switch(Math.floor(Math.random() * 8) + 1){
        case 1:
                $('body').css('background-image', 'url("Img/bcgImg1.dms")');
            break;
        case 2:
                $('body').css('background-image', 'url("Img/bcgImg2.jpg")');
            break;
        case 3:
                $('body').css('background-image', 'url("Img/bcgImg4.jpg")');
            break;
        case 4:
                $('body').css('background-image', 'url("Img/bcgImg5.jpg")');
            break;
        case 5:
                $('body').css('background-image', 'url("Img/bcgImg6.jpg")');
            break;
        case 6:
                $('body').css('background-image', 'url("Img/bcgImg7.jpg")');
            break;
        case 7:
                $('body').css('background-image', 'url("Img/bcgImg8.jpg")');
            break;
        case 8:
            $('body').css('background-image', 'url("Img/bcgImg9.jpg")');
        break;
    }

    //$(".item-toggle").click(function(){
    $('body').on('click', '.item-toggle', function() {
        if($(this).css('background-color')==item_unactive_color)
        {
            $(this).css('background-color', item_active_color);
            $(this).children('.item-status').text("ON");
            $(this).children('.item-image').fadeTo("fast",1);
            $(this).children('.item-header').fadeTo("fast",1);
        }
        else{
            $(this).css('background-color', item_unactive_color);
            $(this).children('.item-status').text("OFF");
            $(this).children('.item-image').fadeTo("slow",0.33);
            $(this).children('.item-header').fadeTo("slow",0.33);

        }
    
    });
  });