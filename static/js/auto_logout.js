/* ==========================================================
   NaNeVora - Auto Logout
========================================================== */

let inactivityTimer;

// 1 Hour
const TIMEOUT = 60 * 60 * 1000;

function resetTimer() {

    clearTimeout(inactivityTimer);

    inactivityTimer = setTimeout(logoutUser, TIMEOUT);

}

function logoutUser() {

    alert("Your session has expired due to inactivity.");

    window.location.href = "/logout/";

}

[
    "mousemove",
    "mousedown",
    "keypress",
    "touchstart",
    "scroll",
    "click"
].forEach(function (event) {

    document.addEventListener(event, resetTimer);

});

resetTimer();