$(document).ready(function() {
  $("#password").on("input", function(e){
    if($("#password").val() == "") {
      $("#password").addClass("is-invalid");
    }
    else {
      $("#password").removeClass("is-invalid");
    }
  });
  $("#user-name").on("input", function(e){
    if($("#user-name").val() == "") { //|| !($("#user-name").val().includes("."))) {
      $("#user-name").addClass("is-invalid");
    }
    else {
      $("#user-name").removeClass("is-invalid");
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
    var userName = finalValidCheck($("#user-name"));
    var password = finalValidCheck($("#password"));
    if(userName && password) {
      $.post("/login", {
          "user_name": $("#user-name").val(),
          "password": $("#password").val(),
          "remember": 0,
        },
        function(result){
          window.location.href = result;
        });
    }
  });
  var parseQueryString = function() {
    var str = window.location.search;
    var objURL = {};
    str.replace(
      new RegExp( "([^?=&]+)(=([^&]*))?", "g" ),
      function( $0, $1, $2, $3 ){
        objURL[ $1 ] = $3;
      }
    );
    return objURL;
  };
  $("body").on("click", "#login", function() {
    var next = parseQueryString()["next"];
    var userName = finalValidCheck($("#user-name"));
    var password = finalValidCheck($("#password"));
    if(userName && password) {
      $.post("/login", {
          "user_name": $("#user-name").val(),
          "password": $("#password").val(),
          "remember": 1,
          "next": next
        },
        function(result){
          window.location.href = result;
        });
    }
  });
});