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

    // Remove commas before sending data to Django
    moneyFields.forEach(function(field){

        field.value = field.value.replace(/,/g,"");

    });

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

function allowOnlyNumbers(id) {

    const input = document.getElementById(id);

    if (!input) return;

    input.addEventListener("input", function () {

        this.value = this.value.replace(/[^0-9]/g, "");

    });

}

allowOnlyNumbers("annual_income");
allowOnlyNumbers("loan_amount");


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
   Currency Fields
========================================== */

const moneyFields = document.querySelectorAll(

'#annual_income, #loan_amount, [name="residential_assets_value"], [name="commercial_assets_value"], [name="luxury_assets_value"], [name="bank_asset_value"]'

);

moneyFields.forEach(function(field){

    field.addEventListener("input", function(){

        let value = this.value.replace(/\D/g,"");

        if(value===""){

            this.value="";

            return;

        }

        this.value = Number(value).toLocaleString("en-IN");

    });

});
/* ==========================================
   Reset Button
========================================== */

const resetBtn = document.getElementById("resetPrediction");

if (resetBtn) {

    resetBtn.addEventListener("click", function () {

        document.getElementById("predictionForm").reset();

    });

}