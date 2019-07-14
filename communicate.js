const {spawn} = require("child_process");
const script = spawn("python", ["communicate.py", "Hello from JavaScript!"]);  // Run Python script with arguments

script.stdout.on("data", function(data) {
    console.log(data.toString());  // Print returned data
});