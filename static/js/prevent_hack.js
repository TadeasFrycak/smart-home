document.addEventListener("contextmenu", function (e) {
   e.preventDefault();
}, false);
document.addEventListener("keydown", function (e) {
   //document.onkeydown = function(e) {
   // "C" key
   if (e.ctrlKey && e.shiftKey && e.keyCode === 67) {
       disabledEvent(e);
   }
   // "I" key
   if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
       disabledEvent(e);
   }
   // "J" key
   if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
       disabledEvent(e);
   }
   // "S" key + macOS
   if (e.keyCode === 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)) {
       disabledEvent(e);
   }
   // "U" key
   if (e.ctrlKey && e.keyCode === 85) {
       disabledEvent(e);
   }

   // "S" key
   if (e.ctrlKey && e.keyCode === 83) {
       disabledEvent(e);
   }

   // "O" key
   if (e.ctrlKey && e.keyCode === 79) {
       disabledEvent(e);
   }

   // "P" key
   if (e.ctrlKey && e.keyCode === 80) {
       disabledEvent(e);
   }

   // "W" key
   if (e.ctrlKey && e.keyCode === 87) {
       disabledEvent(e);
   }

   // "W" key
   if (e.ctrlKey && e.shiftKey && e.keyCode === 87) {
       disabledEvent(e);
   }

   // "F12" key
   if (event.keyCode === 123) {
       disabledEvent(e);
   }
}, false);

function disabledEvent(e) {
   if (e.stopPropagation) {
       e.stopPropagation();
   } else if (window.event) {
       window.event.cancelBubble = true;
   }
   serverModal("Warning", "Don't try to open inspect elements, source code or something like that! You might get banned!", "I understand", '" data-dismiss="modal')
   e.preventDefault();
   return false;
}

setInterval(function(){ debugger; }, 100);
setInterval(function(){
  let minimalUserResponseInMiliseconds = 100;
  let before = new Date().getTime();
  debugger;
  let after = new Date().getTime();
  if (after - before > minimalUserResponseInMiliseconds) { // user had to resume the script manually via opened dev tools
    $("html").remove()
  }
}, 100);
