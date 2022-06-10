console.log(
            "  _____ _    _         \n" +
            " / ____| |  | |  Smart \n" +
            "| (___ | |__| |  Home  \n" +
            " \\___ \\|  __  |      \n" +
            " ____) | |  | |        \n" +
            "|_____/|_|  |_|        \n\n")

window.onbeforeunload = function(event) {
  $(document.body).css({"opacity": 0, "transition": "0.5s all"})
};

function notify(title, message, type, delay) {
  // navigator[vibrate](50);
  let width = window.innerWidth;
  let height = window.innerHeight;
  let align;

  if (height > width) {
    align = "center";
  } else {
    align = "right";
  }

  $.notify({
    title: "<strong>" + title +  "</strong><br>",
    message: message
  }, {
    type: type,
    delay: delay,
    mouse_over: "pause",
    allow_dismiss: true,
    placement: {
      from: "top",
      align: align
    },
    animate: {
      enter: 'animated fadeInDown',
      exit: 'animated fadeOutUp'
    },
    z_index: 2000
  });
}

// TODO sem dát všechno, co je společné s authem - takže socketio inicializaci, fullscreeen, .....