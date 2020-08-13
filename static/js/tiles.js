$(document).ready(function(){
    $(".enable-hammer").each(function(){
        initializeHammerTile(this);
    });

    $(".tile-inner-touch-layer").each(function(){
        initializeInnerHammer(this);
    });
});

function initializeInnerHammer(object) {
    let hammer = new Hammer(object);

    hammer.on("tap", function(el) {
        innerTap(el.target);
    });

    // hammer.on("press", function(el) {
    //     pressed(el.target);
    // });
}

function innerTap(object) {
    let isEditActive = $("body").attr("is_edit_active");

    if (isEditActive === "false") {
        let id = $(object).parent().attr("data-id");
        let innerId = $(object).attr("data-inner-id");
    
        console.log("\r\n--> Inner Tap\r\nID: ");
        console.log(id);
        console.log("inner ID: ");
        console.log(innerId);
        console.log("object");
        console.log($(object));

        // for alarm_clock
        let parent_type = $(object).parent().attr("data-type");
        
        if (parent_type === "alarm_clock") {
            let button_name = $(object).attr("data-inner-id"); 
            let query = button_name.replace("button-","");

            let parent_element = $(object).parent().find(".alarm-clock-glyph[data-type="+ query +"]");

            if (parent_element.hasClass("alarm-clock-glyph-active"))
            {
                console.log("Deactivate " + query);
                parent_element.toggleClass("alarm-clock-glyph-active",false);
            }
            else
            {
                console.log("Activate " + query);
                parent_element.toggleClass("alarm-clock-glyph-active",true);
            }
        }
    }
}

function initializeHammerTile(object) {
    let hammer = new Hammer(object);

    hammer.on("tap", function(el) {
        tapped(el.target);
    });

    hammer.on("press", function(el) {
        pressed(el.target);
    });
}

function tapped(object) {
    // type of item; [toggle/...]
    let tileType = $(object).parent().attr("data-type");
    // "true" = yes; "false" = no
    let isEditActive = $("body").attr("is_edit_active");
    // let id = $(object).parent().attr("data-id");

    let $this = $(object);

    // if edit mode is enabled; edit mode
    if (isEditActive === "true") {
        requestEditModal($this);
    }
    
    // if edit mode is disabled; normal mode
    if (isEditActive === "false") {
        if (tileType === "toggle") tappedOnToggle($this);
    }
}

function pressed(object) {
    // type of item; [toggle/...]
    // let tileType = $(object).parent().attr("data-type");
    // "true" = yes; "false" = no
    let isEditActive = $("body").attr("is_edit_active");
    // let id = $(object).parent().attr("data-id");

    let $this = $(object);

    // if edit mode is enabled; edit mode
    if (isEditActive === "true") {
        // do nothing
    }
    
    // if edit mode is disabled; normal mode
    if (isEditActive === "false") {
        requestNormalModal($this);
    }

}


// CUSTOM EVENTS:
// Po doteku na Toggle tlačítko ( < init.js )
function tappedOnToggle($this) {
    let tileID = $this.parent().attr("data-id");
    let tileState = $this.parent().find(".tile-status").text().toLowerCase() === "on" ? 0 : 1;

    socketio.emit("tile_value", {"id": tileID, "value": tileState});
}