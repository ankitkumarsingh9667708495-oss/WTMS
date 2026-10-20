
document.addEventListener("DOMContentLoaded", function () {
    // Search users by username, email, or other visible row content
    const searchInput = document.getElementById("userSearch");
    const userTable = document.getElementById("userTable");
    const noResults = document.getElementById("noSearchResults");

    if (searchInput && userTable) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase().trim();
            const rows = userTable.querySelectorAll("tbody tr.user-row");
            let visibleCount = 0;

            rows.forEach(function (row) {
                const matches = row.textContent.toLowerCase().includes(query);

                row.style.display = matches ? "" : "none";

                if (matches) {
                    visibleCount++;
                }
            });

            if (noResults) {
                noResults.hidden = visibleCount > 0 || rows.length === 0;
            }
        });
    }

    // Dismiss messages
    document.querySelectorAll(".dismiss-message").forEach(function (button) {
        button.addEventListener("click", function () {
            const message = button.closest(".manage-message");

            if (message) {
                message.remove();
            }
        });
    });

    // Mobile sidebar
    const sidebar = document.getElementById("manageSidebar");
    const menuToggle = document.getElementById("manageMenuToggle");
    const overlay = document.getElementById("manageOverlay");

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
