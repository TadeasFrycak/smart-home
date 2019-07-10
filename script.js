$(document).ready(function(){


    var device_config_array;

    $.get('device-config.txt', function(device_config_data) {
        $.get('items.html.txt', function(items_data){

            device_config_array = device_config_data.split('\n');
            items_data_list = items_data.split('\n');
            //console.log(device_config_array);

            jQuery.each( device_config_array, function( i, val ) {

                if(device_config_array[i].charAt(0) == "-")
                {

                    if (device_config_array[i].indexOf("STAT\"toggle\"") >= 0){ // Je tam toggle button
                        var prepared_item = items_data_list[1];

                        var newStr = device_config_array[i].split('NAME\"')[1].split('\"')[0];
                        prepared_item = prepared_item.replace("<div class='item-header'></div>", "<div class='item-header'>" + newStr + "</div>");

                        var prepared_item_data = device_config_array[i].substring(device_config_array[i].indexOf("NAME"));
                        prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + prepared_item_data + "</div>");
                        
                        $("main").append(prepared_item);   
                    }

                    if (device_config_array[i].indexOf("STAT\"scroll\"") >= 0){ // Je tam scroll button
                        var prepared_item = items_data_list[3];

                        var newStr = device_config_array[i].split('NAME\"')[1].split('\"')[0];
                        prepared_item = prepared_item.replace("<div class=\"item-header\"></div>", "<div class='item-header'>" + newStr + "</div>");

                        var prepared_item_data = device_config_array[i].substring(device_config_array[i].indexOf("NAME"));
                        prepared_item = prepared_item.replace("<div class='item-info'></div>", "<div class='item-info' style='display:none;'>" + prepared_item_data + "</div>");
                        
                        $("main").append(prepared_item);   
                    }


                
                }
            });


        }, 'text');
     }, 'text');




     
        

        

     

     



    var item_unactive_color = 'rgb(206, 206, 206)';
    var item_active_color = 'rgb(255, 255, 255)';


    switch(Math.floor(Math.random() * 7) + 1){
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
    }


    //alert(parseInt(1007,5));

    function map(){}

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
    
    $('body').on('click', '.item-scroll', function() {
        var posY = $(this).position().top;
        
        var konstanta = parseFloat(0.476190476190476);
        
        var overlayYpos = event.pageY - posY - 230;
        var percentage = parseFloat(parseInt(Math.abs((event.pageY - posY - 440))) * konstanta);
        var output = Math.round(percentage / 10) * 10;

        var outputText = "";
        if (output == 0)  outputText = "OFF";
        else outputText = output + "%"; 
        
        $(this).children('.item-status').text(outputText);
        $(".debug").text(Math.round((event.pageY - posY - 230) / 10) * 10);
        $(this).closest('.overlay').prev().append('<style>.overlay:before{top:'+overlayYpos+'px;}</style>');
    });

  });