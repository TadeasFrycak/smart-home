$(document).ready(function(){
    // ----------------------------------------------
    // Process data from Python and apply them
    // ----------------------------------------------


    // Tile statuses
    $(".tileStatus").each(function() {
        if ($(this).text() === "ON"){
        $(this).parent().parent().toggleClass("tileActive");
        $(this).parent().parent().find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");
        }
    });

    $(".GaugeMeter").each(function(test) {
        $(this).gaugeMeter();
    });

    // Tile gauges
    // function createRadGauge(t,e,a,n){function r(t,e,a,n){return{x:t+a*Math.cos(n),y:e+a*Math.sin(n)}}function s(t,e,a,n,s,o){var d=r(t,e,a,-Math.PI),l=r(t,e,a,-Math.PI*(1-1/(o-s)*(n-s))),i=["M",d.x,d.y,"A",a,a,0,0,1,l.x,l.y].join(" ");return i}var o='<svg class="rGauge" viewBox="0 0 200 145"><path class="rGauge-base" id="'+t+'_base" stroke-width="30" /><path class="rGauge-progress" id="'+t+'_progress" stroke-width="30" stroke="#1565c0" /><text class="rGauge-val" id="'+t+'_val" x="100" y="105" text-anchor="middle"></text><text class="rGauge-min-val" id="'+t+'_minVal" x="40" y="125" text-anchor="middle"></text><text class="rGauge-max-val" id="'+t+'_maxVal" x="160" y="125" text-anchor="middle"></text></svg>';document.getElementById(t).innerHTML=o,document.getElementById(t+"_base").setAttribute("d",s(100,100,60,1,0,1)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,e,e,a)),document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var d={setVal:function(r){return r=Math.max(e,Math.min(r,a)),document.getElementById(t+"_progress").setAttribute("d",s(100,100,60,r,e,a)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),d},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("stroke",e),d}};return d}function createVerGauge(t,e,a,n){var r='<svg class="vGauge" viewBox="0 0 145 145"><rect class="vGauge-base" id="'+t+'_base" x="30" y="25" width="30" height="100"></rect><rect class="vGauge-progress" id="'+t+'_progress" x="30" y="25" width="30" height="0" fill="#1565c0"></rect><text class="vGauge-val" id="'+t+'_val" x="70" y="80" text-anchor="start"></text><text class="vGauge-min-val" id="'+t+'_minVal" x="70" y="125"></text><text class="vGauge-max-val" id="'+t+'_maxVal" x="70" y="30" text-anchor="start"></text></svg>';document.getElementById(t).innerHTML=r,document.getElementById(t+"_minVal").textContent=e,document.getElementById(t+"_maxVal").textContent=a;var s={setVal:function(r){r=Math.max(e,Math.min(r,a));var o=100/(a-e)*(r-e);return document.getElementById(t+"_progress").setAttribute("height",o),document.getElementById(t+"_progress").setAttribute("y",25+(100-o)),document.getElementById(t+"_val").textContent=r+(void 0!==n?n:""),s},setColor:function(e){return document.getElementById(t+"_progress").setAttribute("fill",e),s}};return s}

    $(".tile_gauge").each(function(test) {
        var target_id = $(this).attr("data-target_id")
        var min_val = $(this).attr("data-min_val")
        var max_val = $(this).attr("data-max_val")
        var suffix = $(this).attr("data-suffix")
        var color = $(this).    attr("data-color")
        var target_value = $(this).attr("data-target_value")

        // createRadGauge(target_id,min_val,max_val,suffix).setColor(color).setVal(target_value);
    });

    


    // Tile toggles
    $(".tileToggle").each(function(){

        var $this = $(this);

        var mc = new Hammer(this);
        mc.on("tap", function() {
            $this.parent().toggleClass("tileActive");
            // $this.parent().find(".toggle-dot").toggleClass("toggle-dot-update");

            var tile_id = $this.parent().attr("data-id");
            var tile_state = 0;
            tile_state = $this.parent().find(".tileStatus").text();

            if (tile_state === "ON") { $this.parent().find(".tileStatus").text("OFF"); tile_state = 0; $this.parent().find(".toggle-dot").css("background-color","rgba(255, 0, 0, 0.28)");}
            else if (tile_state === "OFF") { $this.parent().find(".tileStatus").text("ON"); tile_state = 1; $this.parent().find(".toggle-dot").css("background-color","rgba(0, 196, 42, 0.28)");}

            $.post("/tile",
            {
                "i": tile_id,
                "v": tile_state
            },
            function(result){});
        });
    });
});