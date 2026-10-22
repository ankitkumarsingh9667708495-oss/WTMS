
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("driverQuickSearch");
    const driverRows = document.querySelectorAll(
        "#driverTable tbody tr[data-driver-row]"
    );
    const noResultsRow = document.getElementById("driverNoResults");

    if (!searchInput) return;

    searchInput.addEventListener("input", function () {
        const searchTerm = searchInput.value.trim().toLowerCase();
        let visibleRows = 0;

        driverRows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();
            const matches = rowText.includes(searchTerm);

            row.style.display = matches ? "" : "none";

            if (matches) {
                visibleRows++;
            }
        });

        if (noResultsRow) {
            noResultsRow.style.display =
                visibleRows === 0 && driverRows.length > 0 ? "" : "none";
        }
    });
});


/* ===== Driver Delete Confirmation Modal ===== */

let driverDeleteTrigger = null;

function openDriverDeleteModal(button) {
    const modal = document.getElementById("driverDeleteModal");
    const form = document.getElementById("driverDeleteForm");
    const nameElement = document.getElementById("driverModalName");
    const confirmButton = document.getElementById("driverModalConfirm");

    if (!modal || !form || !nameElement || !confirmButton) {
        return;
    }

    driverDeleteTrigger = button;

    // Use the existing Django delete URL for the selected driver.
    form.action = button.dataset.deleteUrl;

    // textContent safely displays the driver's name.
    nameElement.textContent = button.dataset.driverName;

    confirmButton.disabled = false;
    confirmButton.textContent = "Delete Driver";

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("driver-modal-open");

    confirmButton.focus();
}

function closeDriverDeleteModal() {
    const modal = document.getElementById("driverDeleteModal");

    if (!modal) {
        return;
    }

    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("driver-modal-open");

    if (driverDeleteTrigger) {
        driverDeleteTrigger.focus();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("driverDeleteModal");
    const form = document.getElementById("driverDeleteForm");
    const confirmButton = document.getElementById("driverModalConfirm");

    if (!modal || !form || !confirmButton) {
        return;
    }

    // Close when clicking the dark background outside the popup.
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeDriverDeleteModal();
        }
    });

    // Close when the Escape key is pressed.
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && modal.classList.contains("is-open")) {
            closeDriverDeleteModal();
        }
    });

    // Prevent repeated clicks while the POST request is submitted.
    form.addEventListener("submit", function () {
        if (!form.checkValidity()) {
            return;
        }

        confirmButton.disabled = true;
        confirmButton.textContent = "Deleting...";
    });
});
