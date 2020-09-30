$(document).ready(function(){
  // TODO přidat podmínku, aby heslo nemohlo obsahovat jméno, příjmení ani username (předtím dát jmeno.lower() a prijmeni.lower() a password.lower() nebo toLowerCase nebo jak je to v JS)

  socketio = io("/com");

  socketio.on("reconnect", function() {
    console.log("Server reconnected! Reloading...");
    location.reload();
  });

  socketio.on("register_result", function(data){
    if (data.status === true)
    {
      window.location.href = $("#register-form").attr("action");
    }  
    else
    {
      console.log("Username is used");  // TODO signalizace tohohle stavu
      $("#register-username").val("");
    }
  });

  $("#register-first-name").focusout(function(){
    validateName($(this));
  });

  $("#register-last-name").focusout(function(){
    validateName($(this));
  });

  $("#register-username").focusout(function(){
    validateUserName();
  });

  // $("#register-password").focusout(function(){
  //   validatePassword();
  // });

  $("#register-password").focusin(function(){
    // $(".password-requirements").css("display","block");
    $(".password-requirements").slideDown( "fast", function() {});
  });
  
  $("#register-password").focusout(function(){
    // $(".password-requirements").css("display","none");
    $(".password-requirements").slideUp( "fast", function() {});
  });
  
  $("#register-password").on("input",function(){
    validatePassword_();
  });
  
  // $("#register-repeat-password").focusout(function(){
  //   validateRepeatPassword();
  // });

  function validateName(object){
    let is_invalid_name = /([^\p{L}])/ug.test($(object).val());
    let result = true;

    if (is_invalid_name) {
      $(object).toggleClass("invalid",true);
      console.log("Invalid characters!");
      result = false
    }
    else {
      $(object).toggleClass("invalid",false); 
    } 

    if ($(object).val()=="") result = false;

    return result

  }

  function validateUserName(){
    let is_invalid_username = /([^a-zA-Z|\d|.|-|_|-]+)/ug.test($("#register-username").val());

    let result = true;

    if (is_invalid_username)
    {
       $("#register-username").toggleClass("invalid",true);
       result = false;
    }
    else 
    {
      $("#register-username").toggleClass("invalid",false);
    }

    if ($("#register-username").val()=="") result = false;

    return result
  }

  function validatePassword_() {

    let element = $("#register-password");
    let second_element = $("#register-repeat-password");
    let chars_label = $("#reg-label-chars");
    let digit_label = $("#reg-label-digit");
    let letter_label = $("#reg-label-letter");

    let passed = true;

    // must contain:
    // 8 chars
    // 1 upper and lower
    // one number

    // one digit:
    let digit_test = /[1-9]/g.test(element.val());
    if (digit_test == true){
      digit_label.toggleClass("register-password-valid", true);
      digit_label.toggleClass("register-password-invalid", false);
    }
    else {
      passed = false;
      digit_label.toggleClass("register-password-valid", false);
      digit_label.toggleClass("register-password-invalid", true);
    }

    // 8 chars:
    let chars_test = /.{8,}/g.test(element.val());
    if (chars_test == true){
      chars_label.toggleClass("register-password-valid", true);
      chars_label.toggleClass("register-password-invalid", false);
    }
    else {
      passed = false;
      chars_label.toggleClass("register-password-valid", false);
      chars_label.toggleClass("register-password-invalid", true);
    }

    // lower and upper:
    let letter_test = /(?=.*[a-z])(?=.*[A-Z])/g.test(element.val());
    if (letter_test == true){
      letter_label.toggleClass("register-password-valid", true);
      letter_label.toggleClass("register-password-invalid", false);
    }
    else {
      passed = false;
      letter_label.toggleClass("register-password-valid", false);
      letter_label.toggleClass("register-password-invalid", true);
    }

    if (element.val() != second_element.val()) passed = false;

    return passed
  }

  // function validatePassword() {
  //   let is_valid_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}/.test($("#register-password").val());

  //   if (!is_valid_password) {
  //     if($("#register-password").val().length > 0)
  //     {
  //       $("#register-password").toggleClass("invalid",true);
  //     }
  //     else $("#register-password").toggleClass("invalid",false);
  //     return false
  //   }
  //   else {
  //     $("#register-password").toggleClass("invalid",false); 
  //     return true
  //   }
  // }


  // function validateRepeatPassword() {
  //   let is_valid_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}/.test($("#register-repeat-password").val());

  //   if (!is_valid_password || $("#register-repeat-password").val() !== $("#register-password").val()) {
  //     if($("#register-repeat-password").val().length > 0)
  //     {
  //       $("#register-repeat-password").toggleClass("invalid",true);
  //     }
  //     else $("#register-repeat-password").toggleClass("invalid",false);
  //     return false
  //   }
  //   else {
  //     $("#register-repeat-password").toggleClass("invalid",false);
  //     return true
  //   }
  // }
  

  $("body").on("click", "#register", function() {
    let validate_fname = validateName($("#register-first-name"));
    let validate_lname = validateName($("#register-last-name"));
    let validate_uname = validateUserName();
    let validate_password = validatePassword_();

    console.log("Validate report:");
    console.log("First name: " + validate_fname);
    console.log("Last name: " + validate_lname);
    console.log("Username: " + validate_uname);
    console.log("Password: " + validate_password);

    if (validate_fname && validate_lname && validate_uname && validate_password)
    {
      console.log("Validation successfull");

      socketio.emit("register", {
        "first_name": $("#register-first-name").val(),
        "last_name": $("#register-last-name").val(),
        "username": $("#register-username").val(),
        "password": $("#register-password").val()
        // "password_repeat": $("#register-repeat-password").val(),
        // "sex": sex
      });
    }


    // if ($("#register-first-name").val() !== "" || $("#register-last-name").val() !== "" || $("#register-username").val() !== "" || $("#register-password").val() !== "" || $("#register-repeat-password").val() !== "") {
    //   if (validateName($("#register-first-name")) && validateName($("#register-last-name")) && validateUserName() && validatePassword() && validateRepeatPassword()) {
    //     let sex = $(".sex:checked").val()
    //     if(sex) {
    //       $(".sex").removeClass("is-invalid");
    //     }
    //     else {
    //       $(".sex").addClass("is-invalid");  // TODO FILIPE tohle nějak přepracuj (i ten design)
    //     }
    //   }
    // }
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
  // if ($("#register-password").val() == $("#register-password-repeat").val()) {
  //     $("#register-password-repeat").removeClass("is-invalid");
  //   }
  //   else {
  //     $("#register-password-repeat").addClass("is-invalid");
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

  // $("#register-password").on("input", function(e){
  //   passwordMatch();
  //     // Validate lowercase letters
  //   let lowerCaseLetters = /[a-z]/g;
  //   let upperCaseLetters = /[A-Z]/g;
  //   let numbers = /[0-9]/g;
  //   if(!$("#register-password").val().match(lowerCaseLetters)) {
  //     $("#register-password").addClass("is-invalid");
  //   }
  //   // Validate capital letters
  //   else if(!$("#register-password").val().match(upperCaseLetters)) {
  //     $("#register-password").addClass("is-invalid");
  //   }

  //   // Validate numbers
  //   else if(!$("#register-password").val().match(numbers)) {
  //     $("#register-password").addClass("is-invalid");
  //   }

  //   // Validate length
  //   else if($("#register-password").val().length <= 8) {
  //     $("#register-password").addClass("is-invalid");
  //   }
  //   else {
  //     $("#register-password").removeClass("is-invalid");
  //   }
  // });

  // $("#register-password-repeat").on("input", function(e){
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

  //   let firstname =


  //   // let firstName = finalValidCheck($("#first-name"));
  //   // let lastName = finalValidCheck($("#last-name"));
  //   // let password = finalValidCheck($("#register-password"));
  //   // let passwordRepeat = finalValidCheck($("#register-password-repeat"));
  //   // let sex = $(".sex:checked").val();
  //   // if(firstName && lastName && password && passwordRepeat && sex) {
  //   //   if(sex) {
  //   //     $(".sex").removeClass("is-invalid");
  //   //     socketio.emit("register", {
  //   //       "firstname": $("#first-name").val(),
  //   //       "lastname": $("#last-name").val(),
  //   //       "user_name": $("#user-name").val(),
  //   //       "permission": $("#permission").text(),
  //   //       "password": $("#register-password").val(),
  //   //       "password_repeat": $("#register-password-repeat").val(),
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

