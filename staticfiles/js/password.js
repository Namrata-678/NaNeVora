/* ==========================================================
   NaNeVora - Password Functions
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       Password Strength
    ========================================== */

    const passwordField = document.getElementById("password1");

    if (passwordField) {

        passwordField.addEventListener("input", checkPasswordStrength);

    }

    /* ==========================================
       Live Password Match
    ========================================== */

    const confirmField = document.getElementById("password2");

    if (passwordField && confirmField) {

        confirmField.addEventListener("input", checkPasswordMatch);

    }

});


/* ==========================================
   Show / Hide Password
========================================== */
function togglePassword(inputId, eyeId) {

    const input = document.getElementById(inputId);
    const eye = document.getElementById(eyeId);

    if (!input || !eye) return;

    if (input.type === "password") {
        input.type = "text";
        eye.classList.remove("fa-eye");
        eye.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        eye.classList.remove("fa-eye-slash");
        eye.classList.add("fa-eye");
    }
}

/* ==========================================
   Password Strength
========================================== */

function checkPasswordStrength() {

    const password = document.getElementById("password1");

    let meter = document.getElementById("passwordStrength");

    if (!password) return;

    if (!meter) {

        meter = document.createElement("small");

        meter.id = "passwordStrength";

        meter.className = "form-text fw-semibold";

        password.parentElement.parentElement.appendChild(meter);

    }

    const value = password.value;

    let score = 0;

    if (value.length >= 8) score++;

    if (/[A-Z]/.test(value)) score++;

    if (/[a-z]/.test(value)) score++;

    if (/[0-9]/.test(value)) score++;

    if (/[^A-Za-z0-9]/.test(value)) score++;

    if (score <= 2) {

        meter.textContent = "Weak Password";

        meter.style.color = "#dc3545";

    }

    else if (score === 3 || score === 4) {

        meter.textContent = "Medium Password";

        meter.style.color = "#ffc107";

    }

    else {

        meter.textContent = "Strong Password";

        meter.style.color = "#198754";

    }

}


/* ==========================================
   Confirm Password Match
========================================== */

function checkPasswordMatch() {

    const password = document.getElementById("password1");

    const confirm = document.getElementById("password2");

    let message = document.getElementById("passwordMatch");

    if (!password || !confirm) return;

    if (!message) {

        message = document.createElement("small");

        message.id = "passwordMatch";

        message.className = "form-text fw-semibold";

        confirm.parentElement.parentElement.appendChild(message);

    }

    if (confirm.value === "") {

        message.textContent = "";

        return;

    }

    if (password.value === confirm.value) {

        message.textContent = "✓ Passwords match";

        message.style.color = "#198754";

    }

    else {

        message.textContent = "✗ Passwords do not match";

        message.style.color = "#dc3545";

    }

}