$(document).ready(function(){
    $(".enable-hammer").each(function(){
        initializeHammerTile(this);
    });

    // $(".tile-inner-touch-layer").each(function(){
    //     initializeInnerHammer(this);
    // });
});

// function initializeInnerHammer(object) {
//     let hammer = new Hammer(object);

//     hammer.on("tap", function(el) {
//         innerTap(el.target);
//     });

//     // hammer.on("press", function(el) {
//     //     pressed(el.target);
//     // });
// }

// function innerTap(object) {
//     let isEditActive = $("body").attr("data-is-edit-active");

//     if (isEditActive === "false") {
//         let id = $(object).parent().attr("data-id");
//         let innerId = $(object).attr("data-inner-id");
    
//         console.log("\r\n--> Inner Tap\r\nID: ");
//         console.log(id);
//         console.log("inner ID: ");
//         console.log(innerId);
//         console.log("object");
//         console.log($(object));

//         // for alarm_clock
//         let parent_type = $(object).parent().attr("data-type");
        
//         if (parent_type === "alarm_clock") {
//             let button_name = $(object).attr("data-inner-id"); 
//             let query = button_name.replace("button-","");

//             let parent_element = $(object).parent().find(".alarm-clock-glyph[data-type="+ query +"]");

//             if (parent_element.hasClass("alarm-clock-glyph-active"))
//             {
//                 console.log("Deactivate " + query);
//                 parent_element.toggleClass("alarm-clock-glyph-active",false);
//             }
//             else
//             {
//                 console.log("Activate " + query);
//                 parent_element.toggleClass("alarm-clock-glyph-active",true);
//             }
//         }
//     }
// }

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
    let isEditActive = $("body").attr("data-is-edit-active");
    // let id = $(object).parent().attr("data-id");

    let $this = $(object);

    // if edit mode is enabled; edit mode
    if (isEditActive === "true") {
        console.log("Requested edit modal");
        requestEditModal($this);
    }
    
    // if edit mode is disabled; normal mode
    if (isEditActive === "false") {
        if (tileType === "toggle") tappedOnToggle($this);
        if (tileType === "alarm_clock") tappedOnAlarmClock($this);
        
    }
}

function pressed(object) {
    // type of item; [toggle/...]
    // let tileType = $(object).parent().attr("data-type");
    // "true" = yes; "false" = no
    let isEditActive = $("body").attr("data-is-edit-active");
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

    socketio.emit("tile_value", {"tile_id": tileID, "value": tileState});
}

function tappedOnAlarmClock($this) {

    // console.log("lkdsjfksdf");
    let tile_element = $this.parent();
    let tileID = $this.parent().attr("data-id");
    // data-active="1"
    // let tileID = $this.parent().attr("data-id");
    // let tileState = $this.parent().find(".tile-status").text().toLowerCase() === "on" ? 0 : 1;

    let is_active = !tile_element.hasClass("tile-active");
    let mon = tile_element.find(".alarm-clock-glyph[data-type='Mon']").hasClass("alarm-clock-glyph-active")
    let tue = tile_element.find(".alarm-clock-glyph[data-type='Tue']").hasClass("alarm-clock-glyph-active")
    let wed = tile_element.find(".alarm-clock-glyph[data-type='Wed']").hasClass("alarm-clock-glyph-active")
    let thu = tile_element.find(".alarm-clock-glyph[data-type='Thu']").hasClass("alarm-clock-glyph-active")
    let fri = tile_element.find(".alarm-clock-glyph[data-type='Fri']").hasClass("alarm-clock-glyph-active")
    let sat = tile_element.find(".alarm-clock-glyph[data-type='Sat']").hasClass("alarm-clock-glyph-active")
    let sun = tile_element.find(".alarm-clock-glyph[data-type='Sun']").hasClass("alarm-clock-glyph-active")


    // console.log("Monday:");
    // console.log(mon);
    // let mon = tile_element.attr("data-mon") === "1";
    // let tue = tile_element.attr("data-tue") === "1";
    // let wed = tile_element.attr("data-wed") === "1";
    // let thu = tile_element.attr("data-thu") === "1";
    // let fri = tile_element.attr("data-fri") === "1";
    // let sat = tile_element.attr("data-sat") === "1";
    // let sun = tile_element.attr("data-sun") === "1";

    console.log("AHAHA");
    console.log(is_active)

    socketio.emit("tile_value", {"tile_id": tileID, "value": {"main": is_active, "monday": mon, "tuesday": tue, "wednesday": wed, "thursday": thu, "friday": fri, "saturday": sat, "sunday": sun}});
}
