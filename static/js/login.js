$(document).ready(function() {
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

  $(document.body).on("click", ".switch-auth", function() {
    toggleAuth();
  });
  $(document.body).on("click", "#login", function() {
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

      $.post("/login", {
        "username": $("#username").val().toLowerCase().trim(),
        "password": $("#password").val(),
        "remember": 1,
      }, function (result) {
        if (result.status) {
          window.location.href = $("#login-form").attr("action");
        }

        else {
          console.log("Wrong username or password");
          notify(_("Login"), _("Username or password is wrong!"), "danger", 5000);

          $(".horizontal-middle").effect("shake");

          $("#username").removeAttr("disabled");
          $("#password").addClass("invalid").removeAttr("disabled").val("");
          setTimeout(() => { $("#password").removeClass("invalid"); }, 3000);
        }
      });
    }
  });
});

function toggleAuth() {
  $(".horizontal-middle").fadeOut("slow", function() {
    $("#login-form").toggle();
    $("#register-form").toggle();
    $(".horizontal-middle").fadeIn("slow");
  });
}