$(document).ready(function() {
  socketio = io("/com");

  socketio.on("reconnect", function() {
    console.log("Server reconnected! Reloading...");
    location.reload();
  });

  socketio.on("login_result", function(data){
    if (data.status === true)
    {
      $.post("/login", {}, function () {
        location.reload();
      });
    }  
    else
    {
      console.log("Wrong password");
      $(this).removeAttr("disabled");
      $("#password").val("");
    }
  });

  $("#password").on("input", function(e){
    if($("#password").val() == "") {
      $("#password").addClass("is-invalid");
    }
    else {
      $("#password").removeClass("is-invalid");
    }
  });

  $("#username").on("input", function(e){
    if($("#username").val() == "") { //|| !($("#user-name").val().includes("."))) {
      $("#username").addClass("is-invalid");
    }
    else {
      $("#username").removeClass("is-invalid");
    }
  });

  $("#password").on("keypress", function (e) {
    if(e.which === 13){
      // Disable textbox to prevent multiple submit
      $(this).attr("disabled", "disabled");
      $("#login").click();
    }
  });

  $("#username").on("keypress", function (e) {
    if(e.which === 13){
      // Disable textbox to prevent multiple submit
      $(this).attr("disabled", "disabled");
      $("#login").click();
    }
  });

  function finalValidCheck(object) {
    if (!$(object).hasClass("is-invalid")) {
      if($(object).val() !== "") {
        return true;
      }
      else {
        $(object).addClass("is-invalid");
      }
    }
    return false;
  }
  $("body").on("click", "#incognito-login", function() {
    // TODO dát dohromady
    // let userName = finalValidCheck($("#username"));
    // let password = finalValidCheck($("#password"));
    // if(userName && password) {
    //   socketio.emit("login", {
    //     "username": $("#username").val(),
    //     "password": $("#password").val(),
    //     "remember": 0,
    //   });
    //   $.post("/login", {}, function(){});
    // }
  });
  let parseQueryString = function() {
    let str = window.location.search;
    let objURL = {};
    str.replace(
      new RegExp( "([^?=&]+)(=([^&]*))?", "g" ),
      function( $0, $1, $2, $3 ){
        objURL[ $1 ] = $3;
      }
    );
    return objURL;
  };
  $("body").on("click", "#login", function() {
    // let next = parseQueryString()["next"];
    let userName = finalValidCheck($("#username"));
    let password = finalValidCheck($("#password"));
    if(userName && password) {
      socketio.emit("login", {
        "username": $("#username").val(),
        "password": $("#password").val(),
        "remember": 1,
        // "next": next
      });
    }
  });
});