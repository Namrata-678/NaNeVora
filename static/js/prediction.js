/* ==========================================================
   NaNeVora - Prediction Page
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const predictionForm = document.getElementById("predictionForm");

    if (!predictionForm) return;

    predictionForm.addEventListener("submit", function (event) {

        if (!validatePredictionForm()) {

            event.preventDefault();

            return;

        }

        showLoading();

    });

});


/* ==========================================
   Prediction Form Validation
========================================== */

function validatePredictionForm() {

    let valid = true;

    const requiredFields = document.querySelectorAll(

        "#predictionForm [required]"

    );

    requiredFields.forEach(function (field) {

        field.classList.remove("is-invalid");

        if (field.value.trim() === "") {

            field.classList.add("is-invalid");

            valid = false;

        }

    });

    return valid;

}


/* ==========================================
   Loading Screen
========================================== */

function showLoading() {

    const overlay = document.getElementById("loadingOverlay");

    const progressBar = document.getElementById("loadingProgress");

    const form = document.getElementById("predictionForm");

    if (overlay) {

        overlay.style.display = "flex";

    }

    /* Disable all form fields */

    form.querySelectorAll("input, select, button").forEach(function (element) {

        element.disabled = true;

    });

    let progress = 0;

    const timer = setInterval(function () {

        progress += 5;

        if (progress > 100) {

            progress = 100;

        }

        progressBar.style.width = progress + "%";

        progressBar.innerHTML = progress + "%";

        if (progress >= 100) {

            clearInterval(timer);

        }

    }, 120);

}

/* ==========================================
   Loan Amount Formatter
========================================== */

const loanAmount = document.getElementById("loan_amount");

if (loanAmount) {

    loanAmount.addEventListener("input", function () {

        let value = this.value.replace(/,/g, "");

        if (!isNaN(value) && value !== "") {

            this.value = Number(value).toLocaleString("en-IN");

        }

    });

}


/* ==========================================
   Annual Income Formatter
========================================== */

const annualIncome = document.getElementById("annual_income");

if (annualIncome) {

    annualIncome.addEventListener("input", function () {

        let value = this.value.replace(/,/g, "");

        if (!isNaN(value) && value !== "") {

            this.value = Number(value).toLocaleString("en-IN");

        }

    });

}


/* ==========================================
   Reset Button
========================================== */

const resetBtn = document.getElementById("resetPrediction");

if (resetBtn) {

    resetBtn.addEventListener("click", function () {

        document.getElementById("predictionForm").reset();

    });

}