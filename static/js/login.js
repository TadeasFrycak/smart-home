$(document).ready(function() {
  socketio.on("login_result", function(data){
    if (data.status === true) {
      $.post("/login", {}, function () {
        window.location.href = $("#login-form").attr("action");
      });
    }
    else {
      console.log("Wrong username or password");
      $("#username").removeAttr("disabled");
      $("#password").removeAttr("disabled");
      $("#password").val("");
    }
  });

  let inputNames = ["#username", "#password"];
  for (let i=0; i < inputNames.length; i++) {
    $(inputNames[i]).bind("cut copy paste", function(e) {
      e.preventDefault();
    });

    $(inputNames[i]).on("keypress", function(e) {
      if(e.which === 13){
        $("#login").click();
      }
    });
  }

  $("#username").on("input", function(e){
    $("#username").val($("#username").val().normalize("NFKD").replace(/[^A-Za-z0-9._-]/g, ""))
  });

  $("body").on("click", "#login", function() {
    let wrong = false;
    let emptyLabels = [];
    if($("#username").val() === "") {
      wrong = true;
      emptyLabels.push(_("Username"))
    }

    if($("#password").val() === "") {
      wrong = true;
      emptyLabels.push(_("Password"))
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
    if (wrong === false) {
      $("#username").attr("disabled", "disabled");
      $("#password").attr("disabled", "disabled");

      socketio.emit("login", {
        "username": $("#username").val().toLowerCase().trim(),
        "password": $("#password").val(),
        "remember": 1,
      });
    }
  });
});