
document.addEventListener("DOMContentLoaded", function () {
    // Mobile sidebar toggle
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", function () {
            const isOpen = sidebar.classList.toggle("open");

            menuToggle.setAttribute(
                "aria-expanded",
                String(isOpen)
            );
        });

        // Close the sidebar after choosing a navigation link on mobile
        sidebar.querySelectorAll(".nav-link").forEach(function (link) {
            link.addEventListener("click", function () {
                sidebar.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });

        // Close the sidebar when clicking outside it
        document.addEventListener("click", function (event) {
            if (
                sidebar.classList.contains("open") &&
                !sidebar.contains(event.target) &&
                !menuToggle.contains(event.target)
            ) {
                sidebar.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    // Display today's date using the browser's local date
    const todayDate = document.getElementById("todayDate");

    if (todayDate) {
        todayDate.textContent = new Intl.DateTimeFormat("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
            weekday: "short"
        }).format(new Date());
    }

    // Search the truck and driver tables
    const searchInput = document.getElementById("dashboardSearch");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.trim().toLowerCase();

            ["truckTable", "driverTable"].forEach(function (tableId) {
                const table = document.getElementById(tableId);

                if (!table) return;

                table.querySelectorAll("tbody tr").forEach(function (row) {
                    const isMatch = row.textContent.toLowerCase().includes(query);
                    row.hidden = !isMatch;
                });
            });
        });
    }
});
