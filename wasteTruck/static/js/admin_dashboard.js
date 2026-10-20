
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("adminSidebar");
    const menuToggle = document.getElementById("adminMenuToggle");
    const overlay = document.getElementById("adminOverlay");

    function openSidebar() {
        if (!sidebar || !menuToggle || !overlay) return;

        sidebar.classList.add("open");
        overlay.classList.add("visible");
        menuToggle.setAttribute("aria-expanded", "true");
    }

    function closeSidebar() {
        if (!sidebar || !menuToggle || !overlay) return;

        sidebar.classList.remove("open");
        overlay.classList.remove("visible");
        menuToggle.setAttribute("aria-expanded", "false");
    }

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            if (sidebar && sidebar.classList.contains("open")) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }

    if (overlay) {
        overlay.addEventListener("click", closeSidebar);
    }

    window.addEventListener("resize", function () {
        if (window.innerWidth > 760) {
            closeSidebar();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });
});
