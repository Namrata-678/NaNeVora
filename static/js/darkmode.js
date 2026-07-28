/* ==========================================================
   NaNeVora - Dark Mode
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const toggleButton = document.getElementById("themeToggle");

    const body = document.body;

    const icon = toggleButton ? toggleButton.querySelector("i") : null;

    /* ==========================================
       Apply Theme
    ========================================== */

    function applyTheme(theme) {

        if (theme === "dark") {

            body.classList.add("dark-mode");

            if (icon) {

                icon.classList.remove("fa-moon");

                icon.classList.add("fa-sun");

            }

        }

        else {

            body.classList.remove("dark-mode");

            if (icon) {

                icon.classList.remove("fa-sun");

                icon.classList.add("fa-moon");

            }

        }

    }

    /* ==========================================
       Load Saved Theme
    ========================================== */

    const savedTheme = localStorage.getItem("theme") || "light";

    applyTheme(savedTheme);

    /* ==========================================
       Toggle Theme
    ========================================== */

    if (toggleButton) {

        toggleButton.addEventListener("click", function () {

            const currentTheme = body.classList.contains("dark-mode")

                ? "dark"

                : "light";

            const newTheme = currentTheme === "dark"

                ? "light"

                : "dark";

            localStorage.setItem("theme", newTheme);

            applyTheme(newTheme);

        });

    }

});