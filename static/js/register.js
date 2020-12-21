$(document).ready(function(){
  // TODO přidat podmínku, aby heslo nemohlo obsahovat jméno, příjmení ani username (předtím dát jmeno.lower() a prijmeni.lower() a password.lower() nebo toLowerCase nebo jak je to v JS)

  socketio.on("register_result", function(data){
    if (data.status === true) {
      toggleAuth();
    }
    else {
      $("#reg-username").removeClass("valid").addClass("invalid");
      setTimeout(() => { $("#reg-username").removeClass("invalid"); }, 3000);
      console.log("Username is taken");
      $("input#reg-username").val("");
    }
  });

  let inputNames = ["#first-reg-name", "#last-reg-name", "#reg-username", "#reg-password", "#repeat-reg-password"];
  for (let i=0; i < inputNames.length; i++) {
    $(inputNames[i]).bind("cut copy paste", function(e) {
      e.preventDefault();
    });

    $(inputNames[i]).on("keypress", function(e) {
      if(e.which === 13){
        $("#register").click();
      }
    });
  }

  $("input#reg-username").on("input", function(e){
    validateUsername("input#reg-username");
  });

  $("input#first-reg-name").on("input", function(e){
    validateName("input#first-reg-name");
  });

  $("input#last-reg-name").on("input", function(e){
    validateName("input#last-reg-name");
  });

  $("input#reg-password").focusin(function(){
    $(".password-requirements").slideDown("fast");
  });
  
  $("input#reg-password").focusout(function(){
    if (validatePassword("input#reg-password")) {
      $(".password-requirements").slideUp("fast");
      $("#reg-password").removeClass("invalid").addClass("valid");
    }
  });
  
  $("input#reg-password").on("input", function(){
    validatePassword("input#reg-password");
  });

  $("input#repeat-reg-password").on("input", function(){
    if (!(validateRepeatPassword("input#reg-password", "input#repeat-reg-password"))) {
      $("input#repeat-reg-password").removeClass("valid").addClass("invalid");
    }
    else {
      $("input#repeat-reg-password").removeClass("invalid").addClass("valid");
    }
  });

  function validateUsername(name) {
    $(name).val($(name).val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, ""));
    return $(name).val() !== "";
  }

  function validateName(name) {
    $(name).val($(name).val().replace(/[^A-Za-z\u00C0-\u024Fˇ´]/g, ""));
    return $(name).val() !== "";
  }

  function validatePassword(passwordInput) {
    let value = $(passwordInput).val();

    let chars_label = $("#reg-label-chars");
    let digit_label = $("#reg-label-digit");
    let letter_label = $("#reg-label-letter");
    let special_label = $("#reg-label-special");

    let passed = true;

    // must contain:
    // 10 chars
    // 1 upper and 1 lower
    // one number
    // one special char

    // one digit:
    let digit_test = /[0-9]/g.test(value);
    if (digit_test === true){
      digit_label.toggleClass("reg-password-valid", true);
      digit_label.toggleClass("reg-password-invalid", false);
    }
    else {
      passed = false;
      digit_label.toggleClass("reg-password-valid", false);
      digit_label.toggleClass("reg-password-invalid", true);
    }

    // 10 chars:
    let chars_test = /.{10,}/g.test(value);
    if (chars_test === true){
      chars_label.toggleClass("reg-password-valid", true);
      chars_label.toggleClass("reg-password-invalid", false);
    }
    else {
      passed = false;
      chars_label.toggleClass("reg-password-valid", false);
      chars_label.toggleClass("reg-password-invalid", true);
    }

    // lower and upper:
    let lowercase_test = /[a-z]/g.test(value);
    let uppercase_test = /[A-Z]/g.test(value);
    if (lowercase_test === true && uppercase_test === true){
      letter_label.toggleClass("reg-password-valid", true);
      letter_label.toggleClass("reg-password-invalid", false);
    }
    else {
      passed = false;
      letter_label.toggleClass("reg-password-valid", false);
      letter_label.toggleClass("reg-password-invalid", true);
    }

    let special_test = /[!@#\$%\^\&*\)\(+=._-]/g.test(value);
    if (special_test === true) {
      special_label.toggleClass("reg-password-valid", true);
      special_label.toggleClass("reg-password-invalid", false);
    }
    else {
      passed = false;
      special_label.toggleClass("reg-password-valid", false);
      special_label.toggleClass("reg-password-invalid", true);
    }

    if (passed === false) {
      $("#reg-password").removeClass("valid").addClass("invalid");
    }
    else {
      $("#reg-password").removeClass("invalid").addClass("valid");
    }
    if (value === "") {
      return null;
    }
    return passed;
  }

  function validateRepeatPassword(passwordInput, repeatInput) {
    if ($(repeatInput).val() === "") {
      return null;
    }
    else return $(repeatInput).val() === $(passwordInput).val();
  }

  function passwordCheck(passInput, unameInput, fnameInput, lnameInput) {
    let pass = $(passInput).val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, "").toLowerCase();
    let uname = $(unameInput).val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, "").toLowerCase();
    let fname = $(fnameInput).val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, "").toLowerCase();
    let lname = $(lnameInput).val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, "").toLowerCase();
    console.log(uname);
    console.log(fname);
    console.log(lname);
    console.log(pass);
    let passed;
    if (uname.length >= 3 && pass.includes(uname)) {
      passed = false;
    }
    else if (fname.length >= 3 && pass.includes(fname)) {
      passed = false;
    }
    else if (lname.length >= 3 && pass.includes(lname)) {
      passed = false;
    }
    else {
      passed = true;
    }
    console.log(passed);
    return passed;
  }

  $(document.body).on("click", "#register", function() {
    let validate_fname = validateName("input#first-reg-name");
    let validate_lname = validateName("input#last-reg-name");
    let validate_uname = validateUsername("input#reg-username");
    let validate_password = validatePassword("input#reg-password");
    let validate_repeat_password = validateRepeatPassword("input#reg-password", "input#repeat-reg-password");
    let password_check = passwordCheck("input#reg-password", "input#reg-username", "input#first-reg-name", "input#last-reg-name");

    let emptyLabels = [];
    if (!validate_fname) {
      emptyLabels.push(_("First name"));
    }
    if (!validate_lname) {
      emptyLabels.push(_("Last name"));
    }
    if (!validate_uname) {
      emptyLabels.push(_("Username"));
    }
    if (validate_password === null) {
      emptyLabels.push(_("Password"));
    }
    else if (validate_password === false) {
      notify(_("Warning"), _("Password must contain all the required characters!"), "warning", 5000);
    }
    else if (!password_check && validate_fname && validate_lname && validate_uname) {
      notify(_("Warning"), _("Password must NOT contain your name or username!"), "warning", 5000);
    }
    if (validate_repeat_password === null) {
      emptyLabels.push(_("Repeat password"));
    }
    else if (validate_repeat_password === false && validate_password) {  // Notify only when password is correct
      notify(_("Warning"), _("Passwords does not match!"), "warning", 5000);
    }

    let emptyString = "";
    for (let i=0; i < emptyLabels.length; i++) {
      if (i === 0) {
        emptyString += emptyLabels[i];
      }
      else if ((i + 1) === emptyLabels.length) {
        emptyString += " " + _("and") + " " + emptyLabels[i].toLowerCase();
      }
      else {
        emptyString += ", " + emptyLabels[i].toLowerCase();
      }
    }

    if (emptyString) {
      emptyString += " cannot be empty";
      notify(_("Warning"), emptyString, "warning", 5000);
    }

    console.log("Validate report:");
    console.log("First name: " + validate_fname);
    console.log("Last name: " + validate_lname);
    console.log("Username: " + validate_uname);
    console.log("Password: " + validate_password);


    if (validate_fname && validate_lname && validate_uname && validate_password && validate_repeat_password && password_check) {
      console.log("Validation successful");

      socketio.emit("register", {
        "first_name": $("input#first-reg-name").val(),
        "last_name": $("input#last-reg-name").val(),
        "username": $("input#reg-username").val().toLowerCase().trim(),
        "password": $("input#reg-password").val()
        // "sex": sex
      });
    }
  });
});

