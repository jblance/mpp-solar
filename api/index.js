var express = require("express");
var bodyParser = require("body-parser");
var app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
const cors = require("cors");
app.use(
  cors({
    origin: "*", //TODO: lock this down with a proper whitelist
  })
);

var mqtt = require("mqtt");

const port = 5000;
app.listen(port, function () {
  console.log("Example app listening at port " + port);
});

app.get("/", (req, res, next) => {
  res.status(200).json("Hello World");
});

app.get("/runCommand", (req, res, next) => {
  var command = req.query.command;
  console.log("Command received: " + command);

  var commandTopic = "mpp-solar/api-client";
  
  //This can be changed if you want to use a different topic for the response
  var responseTopic = command +"/status";
  var tag = "response"

  console.log("ResponseTopic: " + responseTopic);
  var clientCommand = mqtt.connect("mqtt://localhost", {
    clientId: "demo-client",
  });
  clientCommand.on("connect", function () {
    console.log("listening for response on " + responseTopic + "/" + tag);
    clientCommand.subscribe([responseTopic + "/" + tag], { qos: 0 });
  });

  var messageSent = false;  

  clientCommand.on("message", function (topic, message, packet) {
    console.log(message.toString())
    if (topic == responseTopic + "/" + tag) {
      messageSent = true;
      res.setHeader('Content-Type', 'texthtml');
      res.status(200).send(Buffer.from(message.toString()));
      res.end();
    }

    clientCommand.end();
  });

  const commandString = 
  "commands:" + "\n" +
  "- command: " + command + "\n" +
  "  type: basic" + "\n" +
  "  outputs:" + "\n" +
  "  - type: mqtt" + "\n" +
  "    tag: " + tag + "\n" +
  "    topic: " + responseTopic + "\n" +
  "    format: " + "\n" +
  "      type: htmltable" + "\n";
  //const commandJSON = JSON.stringify(commandObj);
  console.log(commandString);

  clientCommand.publish(commandTopic, commandString);

  timer = setTimeout(function () {
    if (!messageSent) {
      console.log("timeout");
      res.status(200).json("no response");
      res.end();
    }
  }, 30000);
});


