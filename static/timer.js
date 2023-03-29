var startTime = new Date().getTime();
var intervalID;

var timerMinutes = 0
var timerSeconds = 0

function startTimer() {
  intervalID = setInterval(function() {
    var currentTime = new Date().getTime();
    var elapsedTime = currentTime - startTime;

    timerMinutes = Math.floor(elapsedTime / (1000 * 60));
    timerSeconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);

    timerMinutes = (timerMinutes < 10 ? "0" : "") + timerMinutes;
    timerSeconds = (timerSeconds < 10 ? "0" : "") + timerSeconds;

    document.getElementById("timer").innerHTML = timerMinutes + ":" + timerSeconds;
  }, 1000);
}

function pauseTimer() {
  clearInterval(intervalID);
}

startTimer(); // start the timer
//pauseTimer(); // pause the timer
