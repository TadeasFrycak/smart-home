$(document).ready(function(){
    // ----------------------------------------------
    // Events
    // ----------------------------------------------

    // Settings icon
    $(document).on("click", "img", function(){
        window.location.href = "edit";
    });

    // Modal toggle button
    $("body").on("change", ".modal_toggle", function(e){
        var object_id = $(this).parent().parent().parent().attr("data-id");
        var object_state = "";
        e.stopPropagation();
        e.stopImmediatePropagation();

        // Checked
        if($(this).prop("checked") === true){
            object_state = "1";
        }

        // Unchecked
        else if($(this).prop("checked") === false){
            object_state = "0";
        }

        value = $("#myModal").data("id-of-caller");

        $.post("/toggle", {
            "i": object_id,
            "v": object_state,
            "id_tile": value
            },
            function(result){});
    });
});
