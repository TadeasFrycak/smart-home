$(document).ready(function(){
  // TODO signalizace co je špatně (FILIPE) - když je is invalid nebo něco takovýho
  // TODO přidat podmínku, aby heslo nemohlo obsahovat jméno, příjmení ani username (předtím dát jmeno.lower() a prijmeni.lower() a password.lower() nebo toLowerCase nebo jak je to v JS)
  // TODO při zmáčknutí enter odeslat registraci, to semé u loginu


  function checkValid(object) {
    if (/^[abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPUQRSTUVWXYZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚÝŽ ]+$/.test(object.val())) {
      $(object).removeClass("is-invalid");
    }
    else {
      $(object).addClass("is-invalid");
    }
  }
  function valueChange() {
    var firstName = $("#first-name").val().toLowerCase().trim().normalize("NFKD").replace(/[^\w]/g, "");
    var lastName = $("#last-name").val().toLowerCase().trim().normalize("NFKD").replace(/[^\w]/g, "");
    if (lastName == "" && firstName == "") {
      $("#user-name").val("");
    }
    else {$("#user-name").val(firstName + "." + lastName);}
  }
  function passwordMatch() {
  if ($("#password").val() == $("#password-repeat").val()) {
      $("#password-repeat").removeClass("is-invalid");
    }
    else {
      $("#password-repeat").addClass("is-invalid");
    }
  }

  function notSame() {
  if ($("#last-name").val() == $("#first-name").val()) {
      $("#last-name").addClass("is-invalid");
    }
    else {
      if ($("#last-name") == "") {
        $("#last-name").removeClass("is-invalid");
      }
    }
  }

  $("#first-name").on("input", function(e){
    valueChange();
    checkValid($("#first-name"));
    notSame();
  });
  $("#last-name").on("input", function(e){
    valueChange();
    checkValid($("#last-name"));
    notSame();
  });

  $("#password").on("input", function(e){
  passwordMatch();
    // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  var upperCaseLetters = /[A-Z]/g;
  var numbers = /[0-9]/g;
  if(!$("#password").val().match(lowerCaseLetters)) {
    $("#password").addClass("is-invalid");
  }
  // Validate capital letters
  else if(!$("#password").val().match(upperCaseLetters)) {
    $("#password").addClass("is-invalid");
  }

  // Validate numbers
  else if(!$("#password").val().match(numbers)) {
    $("#password").addClass("is-invalid");
  }

  // Validate length
  else if($("#password").val().length <= 8) {
    $("#password").addClass("is-invalid");
  }
  else {
    $("#password").removeClass("is-invalid");
  }
  });


  $("#password-repeat").on("input", function(e){
    passwordMatch();
  });

  $(".sex").on("input", function(e){
    $(".sex").removeClass("is-invalid");
  });

  $(".mode").on("input", function(e){
    $(".mode").removeClass("is-invalid");
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
  var dropdownChoosed = false;
  $(".dropdown-menu a").click(function(){
    $("#permission").text($(this).text());
    dropdownChoosed = true;
  });

  $("body").on("click", "#register", function() {
    var firstName = finalValidCheck($("#first-name"));
    var lastName = finalValidCheck($("#last-name"));
    var password = finalValidCheck($("#password"));
    var passwordRepeat = finalValidCheck($("#password-repeat"));
    var sex = $(".sex:checked").val();
    var mode = $(".mode:checked").val();
    if(firstName && lastName && password && passwordRepeat && sex) {
      if(sex && mode) {
        $(".sex").removeClass("is-invalid");
        $.post("/register", {
          "first_name": $("#first-name").val(),
          "last_name": $("#last-name").val(),
          "user_name": $("#user-name").val(),
          "permission": $("#permission").text(),
          "password": $("#password").val(),
          "password_repeat": $("#password-repeat").val(),
          "register_date": new Date(),  // TODO Filipe trochu zformátuj na normální, jako to máme v daterangepicker
          "sex": sex,
          "mode": mode
        },
        function(result){
          window.location.href = result;
        });
      }
    }
    if (!sex) {
      $(".sex").addClass("is-invalid");
    }
    else {
      $(".sex").removeClass("is-invalid");
    }
    if (!mode) {
      $(".mode").addClass("is-invalid");
    }
    else {
      $(".mode").removeClass("is-invalid");
    }
    if(!dropdownChoosed) {
      $("#dropdown-permission").addClass("is-invalid");  // TODO Filipe tohle není nic moc extra, udělj
    }
    else {
      $("#dropdown-permission").removeClass("is-invalid");
    }
  });
});