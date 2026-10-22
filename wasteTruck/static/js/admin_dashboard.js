
/* =========================================
   WTMS Admin Dashboard
   static/js/admin_dashboard.js
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const layout = document.querySelector(".admin-layout");
    const sidebar = document.getElementById("adminSidebar");
    const overlay = document.getElementById("adminOverlay");
    const menuToggle = document.getElementById("adminMenuToggle");

    if (!layout || !sidebar || !overlay || !menuToggle) {
        return;
    }

    function openSidebar() {
        layout.classList.add("sidebar-open");
        menuToggle.setAttribute("aria-expanded", "true");
        menuToggle.setAttribute("aria-label", "Close navigation");
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        layout.classList.remove("sidebar-open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open navigation");
        document.body.style.overflow = "";
    }

    function toggleSidebar() {
        if (layout.classList.contains("sidebar-open")) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    menuToggle.addEventListener("click", toggleSidebar);

    overlay.addEventListener("click", closeSidebar);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });

    // Close the mobile sidebar after choosing a navigation link.
    sidebar.querySelectorAll(".admin-nav-link").forEach(function (link) {
        link.addEventListener("click", function () {
            closeSidebar();
        });
    });

    // If the screen is resized to desktop, reset mobile menu state.
    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) {
            closeSidebar();
        }
    });
});
