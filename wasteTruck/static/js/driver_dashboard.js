
document.addEventListener("DOMContentLoaded", function () {
    // Display today's date
    const todayDate = document.getElementById("todayDate");

    if (todayDate) {
        todayDate.textContent = new Date().toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });
    }

    // Mobile sidebar controls
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    function openSidebar() {
        if (!sidebar || !menuToggle || !sidebarOverlay) return;

        sidebar.classList.add("open");
        sidebarOverlay.classList.add("visible");
        menuToggle.setAttribute("aria-expanded", "true");
    }

    function closeSidebar() {
        if (!sidebar || !menuToggle || !sidebarOverlay) return;

        sidebar.classList.remove("open");
        sidebarOverlay.classList.remove("visible");
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

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", closeSidebar);
    }

    // Highlight the selected sidebar link
    const navLinks = document.querySelectorAll(".sidebar-nav .nav-link");

    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.forEach(function (item) {
                item.classList.remove("active");
            });

            link.classList.add("active");
            closeSidebar();
        });
    });

    // Search collection tasks
    const taskSearch = document.getElementById("taskSearch");
    const taskTable = document.getElementById("taskTable");

    if (taskSearch && taskTable) {
        taskSearch.addEventListener("input", function () {
            const query = taskSearch.value.toLowerCase().trim();
            const rows = taskTable.querySelectorAll("tbody tr:not(.empty-row)");

            rows.forEach(function (row) {
                const rowText = row.textContent.toLowerCase();

                row.classList.toggle(
                    "hidden-row",
                    !rowText.includes(query)
                );
            });
        });
    }

    // Close sidebar when returning to desktop layout
    window.addEventListener("resize", function () {
        if (window.innerWidth > 760) {
            closeSidebar();
        }
    });

    // Close sidebar with Escape
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });
});
