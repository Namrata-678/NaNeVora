/* ==========================================================
   NaNeVora - Prediction Page
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const predictionForm = document.getElementById("predictionForm");

    if (!predictionForm) return;

    /* ==========================================
       Money Fields
    ========================================== */

    const moneyFields = document.querySelectorAll(
        '#annual_income, #loan_amount, [name="residential_assets_value"], [name="commercial_assets_value"], [name="luxury_assets_value"], [name="bank_asset_value"]'
    );

    moneyFields.forEach(function (field) {

        field.addEventListener("input", function () {

            // Keep only digits
            let value = this.value.replace(/\D/g, "");

            if (value === "") {
                this.value = "";
                return;
            }

            // Format in Indian style
            this.value = Number(value).toLocaleString("en-IN");

        });

    });

    /* ==========================================
       Form Submit
    ========================================== */

    predictionForm.addEventListener("submit", function (event) {

        if (!validatePredictionForm()) {

            event.preventDefault();
            return;

        }

        // Remove commas before sending to Django
        moneyFields.forEach(function (field) {

            field.value = field.value.replace(/,/g, "");

        });

        showLoading();

    });

});


/* ==========================================
   Validation
========================================== */

function validatePredictionForm() {

    let valid = true;

    const requiredFields = document.querySelectorAll("#predictionForm [required]");

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

    if (overlay) {

        overlay.style.display = "flex";

    }

    const predictBtn = document.getElementById("predictBtn");

    if (predictBtn) {

        predictBtn.disabled = true;

    }

    let progress = 0;

    const timer = setInterval(function () {

        progress += 5;

        if (progress > 100) progress = 100;

        progressBar.style.width = progress + "%";
        progressBar.innerHTML = progress + "%";

        if (progress >= 100) {

            clearInterval(timer);

        }

    }, 120);

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