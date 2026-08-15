/* ==========================================================
   NaNeVora - Main JavaScript
   Common functions used throughout the website
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       Sticky Navbar Shadow
    ========================================== */

    const navbar = document.querySelector(".custom-navbar");

    if (navbar) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 50) {

                navbar.classList.add("navbar-scrolled");

            } else {

                navbar.classList.remove("navbar-scrolled");

            }

        });

    }


    /* ==========================================
       Active Navigation Link
    ========================================== */

    const currentPath = window.location.pathname;

    document.querySelectorAll(".navbar-nav .nav-link").forEach(link => {

        if (link.getAttribute("href") === currentPath) {

            link.classList.add("active");

        }

    });


    /* ==========================================
       Scroll To Top Button
    ========================================== */

    const scrollButton = document.getElementById("scrollTopBtn");

    if (scrollButton) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 300) {

                scrollButton.style.display = "flex";

            } else {

                scrollButton.style.display = "none";

            }

        });

        scrollButton.addEventListener("click", function () {

            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });

        });

    }


    /* ==========================================
       Smooth Scroll for Anchor Links
    ========================================== */

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                e.preventDefault();

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });


    /* ==========================================
       Auto Close Bootstrap Alerts
    ========================================== */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.classList.remove("show");

            alert.classList.add("fade");

        }, 5000);

    });


    /* ==========================================
       Fade-in Animation on Scroll
    ========================================== */

    const animatedElements = document.querySelectorAll(

        ".fade-left, .fade-right, .fade-up"

    );

    const observer = new IntersectionObserver(

        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.classList.add("show");

                }

            });

        },

        {

            threshold: 0.15

        }

    );

    animatedElements.forEach(element => {

        observer.observe(element);

    });


    /* ==========================================
       Disable Multiple Form Submissions
    ========================================== */

    document.querySelectorAll("form").forEach(form => {

        form.addEventListener("submit", function () {

            const button = form.querySelector("button[type='submit']");

            if (button) {

                button.disabled = true;

                button.innerHTML =

                    '<i class="fas fa-spinner fa-spin"></i> Please Wait...';

            }

        });

    });

});