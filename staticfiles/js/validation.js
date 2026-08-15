/* ==========================================================
   NaNeVora - Form Validation
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            if (!validateForm(form)) {

                event.preventDefault();

            }

        });

    });

});


/* ==========================================
   Main Validation
========================================== */

function validateForm(form) {

    let valid = true;

    clearErrors(form);

    const requiredFields = form.querySelectorAll("[required]");

    requiredFields.forEach(function (field) {

        const value = field.value.trim();

        if (value === "") {

            showError(field, "This field is required.");

            valid = false;

            return;

        }

        /* Email */

        if (field.type === "email") {

            if (!isValidEmail(value)) {

                showError(field, "Enter a valid email address.");

                valid = false;

            }

        }

        /* Phone */

        if (field.name.toLowerCase().includes("phone")) {

            if (!isValidPhone(value)) {

                showError(field, "Phone number must contain 10 digits.");

                valid = false;

            }

        }

        /* Income */

        if (field.name.toLowerCase().includes("income")) {

            if (Number(value) <= 0) {

                showError(field, "Income must be greater than zero.");

                valid = false;

            }

        }

        /* Loan Amount */

        if (field.name.toLowerCase().includes("loan")) {

            if (Number(value) <= 0) {

                showError(field, "Loan amount must be greater than zero.");

                valid = false;

            }

        }

    });

    /* Password Match */

/* Password Match */

const password = form.querySelector(
    "[name='password'], [name='password1'], [name='new_password1']"
);

const confirm = form.querySelector(
    "[name='confirm_password'], [name='password2'], [name='new_password2']"
);

if (password && confirm) {

    if (password.value !== confirm.value) {

        showError(confirm, "Passwords do not match.");

        valid = false;

    }

}

    return valid;

}


/* ==========================================
   Email Validation
========================================== */

function isValidEmail(email) {

    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);

}


/* ==========================================
   Phone Validation
========================================== */

function isValidPhone(phone) {

    const pattern = /^[0-9]{10}$/;

    return pattern.test(phone);

}


/* ==========================================
   Show Error
========================================== */

function showError(field, message) {

    field.classList.add("is-invalid");

    const error = document.createElement("div");

    error.className = "invalid-feedback";

    error.innerText = message;

    field.parentNode.appendChild(error);

}


/* ==========================================
   Remove Previous Errors
========================================== */

function clearErrors(form) {

    form.querySelectorAll(".invalid-feedback").forEach(function (error) {

        error.remove();

    });

    form.querySelectorAll(".is-invalid").forEach(function (field) {

        field.classList.remove("is-invalid");

    });

}