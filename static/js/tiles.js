$(document).ready(function(){

    $(".enableHammer").each(function(){
        initializeHammerTile(this);
    });

});

function initializeHammerTile(object)
{
    var hammer = new Hammer(object);

    hammer.on("tap", function(el) {
        tapped(el.target);
    });

    hammer.on("press", function(el) {
        pressed(el.target);
    });
}

function tapped(object)
{
    // type of item; [toggle/...]
    var tileType = $(object).parent().attr("data-type");
    // "true" = yes; "false" = no
    var isEditActive = $("body").attr("is_edit_active");
    var id = $(object).parent().attr("data-id");

    var $this = $(object);

    // if edit mode is enabled; edit mode
    if (isEditActive == "true")
    {
        requestEditModal($this);
    }
    
    // if edit mode is disabled; normal mode
    if (isEditActive == "false")
    {
        if (tileType == "toggle") tappedOnToggle($this);   
    }

}

function pressed(object)
{
    // type of item; [toggle/...]
    var tileType = $(object).parent().attr("data-type");
    // "true" = yes; "false" = no
    var isEditActive = $("body").attr("is_edit_active");
    var id = $(object).parent().attr("data-id");

    var $this = $(object);

    // if edit mode is enabled; edit mode
    if (isEditActive == "true")
    {
        // do nothing
    }
    
    // if edit mode is disabled; normal mode
    if (isEditActive == "false")
    {
        requestNormalModal($this);
    }

}


// CUSTOM EVENTS:

// Po doteku na Toggle tlačítko ( < init.js )
function tappedOnToggle($this)
{
    $this.parent().toggleClass("tileActive");
    var tileID = $this.parent().attr("data-id");
    var tileState = $this.parent().find(".tileStatus").text().toLowerCase() == "on" ? 1 : 0;

    if (tileState === 1) {
        tileState = 0;
        $this.parent().find(".tileStatus").text("Off");
        //$this.parent().css("opacity", 0.7);
        // TODO NASTAVENÍ
        //$this.parent().css({"-moz-transform": "scale(1)", "-webkit-transform": "scale(1)", "transform": "scale(1)"})
        $this.parent().find(".toggle-dot").css("background-color", "rgba(255, 0, 0, 0.28)");
    }
    else if (tileState === 0) {
        tileState = 1;
        $this.parent().find(".tileStatus").text("On");
        //$this.parent().css("opacity", 1);
        // TODO NASTAVENÍ
        //$this.parent().css({"-moz-transform": "scale(1.03)", "-webkit-transform": "scale(1.03)", "transform": "scale(1.03)"})
        $this.parent().find(".toggle-dot").css("background-color", "rgba(0, 196, 42, 0.28)");
    }

    $.post("/tile", {
        "id": tileID,
        "value": tileState
    }
    );
  
}