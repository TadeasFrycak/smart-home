$(document).ready(function(){

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

    $(".item-toggle").click(function(){
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
    
    $('.item-scroll').click(function(e) {
        var posX = $(this).position().left,posY = $(this).position().top;
        //alert( (e.pageX - posX) + ' , ' + (e.pageY - posY));
        
        var konstanta = parseFloat(0.476190476190476);
        
        var overlayYpos = e.pageY - posY - 230;
        var percentage = parseFloat(parseInt(Math.abs((e.pageY - posY - 440))) * konstanta);
        var output = Math.round(percentage / 10) * 10;

        var outputText = "";
        if (output == 0)  outputText = "OFF";
        else outputText = output + "%"; 
        
        $(this).children('.item-status').text(outputText);
        $(".debug").text(Math.round((e.pageY - posY - 230) / 10) * 10);
        $('.overlay').append('<style>.overlay:before{top:'+overlayYpos+'px;}</style>');
        // 0 = 0%; 210 = 100%
        // 230;440
    });

  });