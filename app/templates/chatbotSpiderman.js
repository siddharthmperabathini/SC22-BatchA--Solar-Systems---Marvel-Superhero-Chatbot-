//links
//http://eloquentjavascript.net/09_regexp.html
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
//requires jquerry

var messages = [], //array that hold the record of each string in chat
  lastUserMessage = "", //keeps track of the most recent input string from the user
  botMessage = "", //var keeps track of what the chatbot is going to say
  botName = 'Chatbot', //name of the chatbot
  talking = true; //when false the speach function doesn't work

function getCookie(c_name)
{
    if(typeof localStorage != "undefined")
    {
        return localStorage.getItem(c_name);
    }
    else
    {
        var c_start = document.cookie.indexOf(c_name + "=");
        if (document.cookie.length > 0)
        {
            if (c_start !== -1)
            {
                return getCookieSubstring(c_start, c_name);
            }
        }
        return "";
    }
}

function setCookie(c_name, value, expiredays)
{
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    if(typeof localStorage != "undefined")
    {
        alert("This place has local storage!");
        localStorage.setItem(c_name, value);
    }
    else
    {
        alert("No local storage here");
        document.cookie = c_name + "=" + escape(value) +
        ((expiredays === null) ? "" : ";expires=" + exdate.toUTCString());
    }
}
//
//
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//edit this function to change what the chatbot says
function chatbotSpidermanResponse() {
  talking = true;
  botMessage = response;

}
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//****************************************************************
//
//
//
//this runs each time enter is pressed.
//It controls the overall input and output
function newEntry() {
  //if the message from the user isn't empty then run 
  if (document.getElementById("chatbox").value != "") {
    //pulls the value from the chatbox ands sets it to lastUserMessage
    lastUserMessage = document.getElementById("chatbox").value;

    setCookie("spidermanAICAMP", getCookie("spidermanAICAMP")+"^^You :"+lastUSerMessage)
    //sets the chat box to be clear
    document.getElementById("chatbox").value = "";

    //adds the value of the chatbox to the array messages
    messages.push(lastUserMessage);

    //Speech(lastUserMessage);  //says what the user typed outloud
    //sets the variable botMessage in response to lastUserMessage
    chatbotSpidermanResponse();

    //add the chatbot's name and message to the array messages
    messages.push("<b>" + botName + ":</b> " + botMessage);

    // says the message using the text to speech function written below
    // Speech(botMessage);
    //outputs the last few array elements of messages to html
    for (var i = 1; i < 8; i++) {
      if (messages[messages.length - i])
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
    }
  }
}

//text to Speech
//https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
function Speech(say) {
  if ('speechSynthesis' in window && talking) {
    var utterance = new SpeechSynthesisUtterance(say);
    //msg.voice = voices[10]; // Note: some voices don't support altering params
    //msg.voiceURI = 'native';
    //utterance.volume = 1; // 0 to 1
    //utterance.rate = 0.1; // 0.1 to 10
    //utterance.pitch = 1; //0 to 2
    //utterance.text = 'Hello World';
    //utterance.lang = 'en-US';
    speechSynthesis.speak(utterance);
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    //runs this function when enter is pressed
    newEntry();
  }
  if (key == 38) {
    console.log('hi')
      //document.getElementById("chatbox").value = lastUserMessage;
  }
}

//clears the placeholder text ion the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}
$(document).ready(function() {
  //Call your function here
  cookie = getCookie("spidermanCookieAICAMP");
  text = cookie.split("^^"); //array of user response then bot it alternating fasion ie [user input, bot response, user input,...]
  //code here to populate the chat boxes with the previous converstation
  messages = text;
  for (var i = 1; i < 8; i++) {
      if (messages[messages.length - i])
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];

    }
});