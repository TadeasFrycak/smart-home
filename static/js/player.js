$(document).ready(function(){
  var marq = [];

  $(".play").show();
  $(".stop").hide();
  var music = new Audio("music/Bon Jovi - Its My Life.mp3");
  //var prank = new Audio("static/music/Hymna Ruské federace - Гимн России.mp3");
  //prank.play();
  $("body").on("click", ".stop", function(e) {
    $(".stop").show().fadeOut("slow");
    $(".play").hide().fadeIn("slow");

    var thumbnail = document.querySelector('#thumbnail');
    thumbnail.style.transform = "scale(1)";
    music.animate({volume: 0}, 1000);

    marq[0].end();
    marq.length = 0;
  });

  $("body").on("click", ".play", function(e) {
    $(".play").show().fadeOut("slow");
    $(".stop").hide().fadeIn("slow");
    music.play();
    var thumbnail = document.querySelector('#thumbnail');

    thumbnail.style.transform = "scale(1.1)";
    thumbnail.style.top = "10px"

    music.animate({volume: 1}, 1000);

    marquee = new Marquee('music_name', {
    // once or continuous
    continuous: true,
    // 'rtl' or 'ltr'
    direction: 'rtl',
    // pause between loops
    delayAfter: 0,
    // when to start
    delayBefore: 0,
    // scroll speed
    speed: 0.1,
    // loops
    loops: -1
  });

  marq.push(marquee);

  });


  function updateProgressValue() {
      var progress = document.querySelector('.music-track-02el');
      progress.style.width = music.currentTime / music.duration * 100+ "px";

  };

  //setInterval(updateProgressValue, 500);
});

var Marquee = function(element, defaults) {
  "use strict";

  var elem = document.getElementById(element),
    options = (defaults === undefined) ? {} : defaults,
    continuous = options.continuous || true, // once or continuous
    delayAfter = options.delayAfter || 1000, // pause between loops
    delayBefore = options.delayBefore || 0, // when to start
    direction = options.direction || 'ltr', // ltr or rtl
    loops = options.loops || -1,
    speed = options.speed || 0.5,
    timer = null,
    milestone = 0,
    marqueeElem = null,
    elemWidth = null,
    self = this,
    ltrCond = 0,
    loopCnt = 0,
    start = 0,
    process = null,
    constructor = function(elem) {

      // Build html
      var elemHTML = elem.innerHTML,
        elemNode = elem.childNodes[1] || elem;

      elemWidth = elemNode.offsetWidth;

      marqueeElem = '<div>' + elemHTML + '</div>';
      elem.innerHTML = marqueeElem;
      marqueeElem = elem.getElementsByTagName('div')[0];
      elem.style.overflow = 'hidden';
      marqueeElem.style.whiteSpace = 'nowrap';
      marqueeElem.style.position = 'relative';

      if (continuous === true) {
        marqueeElem.innerHTML += elemHTML;
        marqueeElem.style.width = '200%';

        if (direction === 'ltr') {
          start = -elemWidth;
        }
      } else {
        ltrCond = elem.offsetWidth;

        if (direction === 'rtl') {
          milestone = ltrCond;
        }
      }

      if (direction === 'ltr') {
        milestone = -elemWidth;
      } else if (direction === 'rtl') {
        speed = -speed;
      }

      self.start();

      return marqueeElem;
    }

  this.start = function() {
    process = window.setInterval(function() {
      self.play();
    });
  };

  this.play = function() {
    // beginning
    marqueeElem.style.left = start + 'px';
    start = start + speed;

    if (start > ltrCond || start < -elemWidth) {
      start = milestone;
      loopCnt++;

      if (loops !== -1 && loopCnt >= loops) {
        marqueeElem.style.left = 0;
      }
    }
  }

  this.end = function() {
    window.clearInterval(process);
  }

  // Init plugin
  marqueeElem = constructor(elem);
}

/*
window.onload = function() {

  var file = document.getElementById("thefile");
  var audio = document.getElementById("audio");
  console.log(file.files);
  file.onchange = function() {
   $(".bcg-real").show().fadeOut(2000);
    setTimeout(() => {
    var files = this.files;

    audio.src = URL.createObjectURL(files[0]);
    audio.load();
    audio.play();
    var context = new AudioContext();
    var src = context.createMediaElementSource(audio);
    var analyser = context.createAnalyser();

    var canvas = document.getElementById("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext("2d");

    src.connect(analyser);
    analyser.connect(context.destination);

    analyser.fftSize = 256;

    var bufferLength = analyser.frequencyBinCount;
    console.log(bufferLength);

    var dataArray = new Uint8Array(bufferLength);

    var WIDTH = canvas.width;
    var HEIGHT = canvas.height;

    var barWidth = (WIDTH / bufferLength) * 2.5;
    var barHeight;
    var x = 0;

    function renderFrame() {
      requestAnimationFrame(renderFrame);

      x = 0;

      analyser.getByteFrequencyData(dataArray);

      ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      for (var i = 0; i < bufferLength; i++) {
        barHeight = dataArray[i];

        var r = barHeight + (25 * (i/bufferLength));
        var g = 250 * (i/bufferLength);
        var b = 50;

        ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
        ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

        x += barWidth + 1;
      }
    }

    audio.play();
    renderFrame();
    }, 2000);
  };
};*/