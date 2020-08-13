$(document).ready(function(){
  // TODO signalizace co je špatně (FILIPE) - když začnu upravovat input tak aby zmizla červená barva textu
  // TODO přidat podmínku, aby heslo nemohlo obsahovat jméno, příjmení ani username (předtím dát jmeno.lower() a prijmeni.lower() a password.lower() nebo toLowerCase nebo jak je to v JS)

  socketio = io("/com");

  socketio.on("register_result", function(data){
    if (data.status === true)
    {
      window.location.href = $("#register-form").attr("action");
    }  
    else
    {
      console.log("Username is used");  // TODO signalizace tohohle stavu
      $("#username").val("");
    }
  });

  $("#first_name").focusout(function(){
    validateName($(this));
  });

  $("#last_name").focusout(function(){
    validateName($(this));
  });

  function validateName(object){
    let is_invalid_first_name = /([^\p{L}])/ug.test($(object).val());

    if (is_invalid_first_name) {
      $(object).toggleClass("invalid",true);
      console.log("Invalid characters!");
      return false
    }
    else {
      $(object).toggleClass("invalid",false); 
      return true
    } 
  }

  $("#username").focusout(function(){
    validateUserName();
  });

  function validateUserName(){
    let is_invalid_username = /([^a-zA-Z|\d|.|-|_|-]+)/ug.test($("#username").val());

    if (is_invalid_username)
    {
       $("#username").toggleClass("invalid",true);
       return false
    }
    else 
    {
      $("#username").toggleClass("invalid",false);
      return true
    }
  }

  $("#password").focusout(function(){
    validatePassword();
  });

  function validatePassword() {
    let is_valid_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}/.test($("#password").val());

    if (!is_valid_password) {
       $("#password").toggleClass("invalid",true);
       return false
    }
    else {
      $("#password").toggleClass("invalid",false); 
      return true
    }
  }

  $("#repeat_password").focusout(function(){
    validateRepeatPassword();
  });

  function validateRepeatPassword() {
    let is_valid_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}/.test($("#repeat_password").val());

    if (!is_valid_password || $("#repeat_password").val() !== $("#password").val()) {
      $("#repeat_password").toggleClass("invalid",true);
      return false
    }
    else {
      $("#repeat_password").toggleClass("invalid",false);
      return true
    }
  }
  

  $("body").on("click", "#register", function() {
    if ($("#first_name").val() !== "" || $("#last_name").val() !== "" || $("#username").val() !== "" || $("#password").val() !== "" || $("#repeat_password").val() !== "") {
      if (validateName($("#first_name")) && validateName($("#last_name")) && validateUserName() && validatePassword() && validateRepeatPassword()) {
        let sex = $(".sex:checked").val()
        if(sex) {
          $(".sex").removeClass("is-invalid");
          socketio.emit("register", {
            "first_name": $("#first_name").val(),
            "last_name": $("#last_name").val(),
            "username": $("#username").val(),
            "password": $("#password").val(),
            "password_repeat": $("#repeat_password").val(),
            "sex": sex
          });
        }
        else {
          $(".sex").addClass("is-invalid");  // TODO FILIPE tohle nějak přepracuj (i ten design)
        }
      }
    }
  });





  // function checkValid(object) {
  //   if (/^[abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPUQRSTUVWXYZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚÝŽ ]+$/.test(object.val())) {
  //     $(object).removeClass("is-invalid");
  //   }
  //   else {
  //     $(object).addClass("is-invalid");
  //   }
  // }
  // function valueChange() {
  //   let firstName = $("#first-name").val().toLowerCase().trim().normalize("NFKD").replace(/[^\w]/g, "");
  //   let lastName = $("#last-name").val().toLowerCase().trim().normalize("NFKD").replace(/[^\w]/g, "");
  //   if (lastName == "" && firstName == "") {
  //     $("#user-name").val("");
  //   }
  //   else {$("#user-name").val(firstName + "." + lastName);}
  // }
  // function passwordMatch() {
  // if ($("#password").val() == $("#password-repeat").val()) {
  //     $("#password-repeat").removeClass("is-invalid");
  //   }
  //   else {
  //     $("#password-repeat").addClass("is-invalid");
  //   }
  // }

  // function notSame() {
  //   var firstName = $("#first-name").val();
  //   var lastName = $("#last-name").val();

  //   if ((firstName == lastName) || firstName.includes(lastName) || lastName.includes(firstName)) {
  //     $("#last-name").addClass("is-invalid");
  //   }
  //   else {
  //     if ($("#last-name") == "") {
  //       $("#last-name").removeClass("is-invalid");
  //     }
  //   }
  // }

  // $("#first-name").on("input", function(e){
  //   valueChange();
  //   checkValid($("#first-name"));
  //   notSame();
  // });
  // $("#last-name").on("input", function(e){
  //   valueChange();
  //   checkValid($("#last-name"));
  //   notSame();
  // });

  // $("#password").on("input", function(e){
  //   passwordMatch();
  //     // Validate lowercase letters
  //   let lowerCaseLetters = /[a-z]/g;
  //   let upperCaseLetters = /[A-Z]/g;
  //   let numbers = /[0-9]/g;
  //   if(!$("#password").val().match(lowerCaseLetters)) {
  //     $("#password").addClass("is-invalid");
  //   }
  //   // Validate capital letters
  //   else if(!$("#password").val().match(upperCaseLetters)) {
  //     $("#password").addClass("is-invalid");
  //   }

  //   // Validate numbers
  //   else if(!$("#password").val().match(numbers)) {
  //     $("#password").addClass("is-invalid");
  //   }

  //   // Validate length
  //   else if($("#password").val().length <= 8) {
  //     $("#password").addClass("is-invalid");
  //   }
  //   else {
  //     $("#password").removeClass("is-invalid");
  //   }
  // });

  // $("#password-repeat").on("input", function(e){
  //   passwordMatch();
  // });

  // $(".sex").on("input", function(e){
  //   $(".sex").removeClass("is-invalid");
  // });

  // function finalValidCheck(object) {
  //   if (!$(object).hasClass("is-invalid")) {
  //     if($(object).val() !== "") {
  //       return true;
  //     }
  //     else {
  //       $(object).addClass("is-invalid");
  //     }
  //   }
  //   return false;
  // }
  // let dropdownChoosed = false;
  // $(".dropdown-menu a").click(function(){
  //   $("#permission").text($(this).text());
  //   dropdownChoosed = true;
  // });

  // $("body").on("click", "#register", function() {

  //   let first_name =


  //   // let firstName = finalValidCheck($("#first-name"));
  //   // let lastName = finalValidCheck($("#last-name"));
  //   // let password = finalValidCheck($("#password"));
  //   // let passwordRepeat = finalValidCheck($("#password-repeat"));
  //   // let sex = $(".sex:checked").val();
  //   // if(firstName && lastName && password && passwordRepeat && sex) {
  //   //   if(sex) {
  //   //     $(".sex").removeClass("is-invalid");
  //   //     socketio.emit("register", {
  //   //       "first_name": $("#first-name").val(),
  //   //       "last_name": $("#last-name").val(),
  //   //       "user_name": $("#user-name").val(),
  //   //       "permission": $("#permission").text(),
  //   //       "password": $("#password").val(),
  //   //       "password_repeat": $("#password-repeat").val(),
  //   //       "register_date": new Date(),  // TODO Filipe trochu zformátuj na normální, jako to máme v daterangepicker
  //   //       "sex": sex
  //   //     });
  //   //   }
  //   //   else {
  //   //     $(".sex").addClass("is-invalid");
  //   //   }
  //   // }

  //   // if(!dropdownChoosed) {
  //   //   $("#dropdown-permission").addClass("is-invalid");  // TODO Filipe tohle není nic moc extra, udělj a přesuň to nahoru a uprav všechno na dropdawn nebo něco podobnýho
  //   // }
  //   // else {
  //   //   $("#dropdown-permission").removeClass("is-invalid");
  //   // }
  // });
});

