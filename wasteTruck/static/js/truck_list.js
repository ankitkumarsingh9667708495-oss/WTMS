
document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".truck-message");

    messages.forEach(function (message) {
        window.setTimeout(function () {
            message.classList.add("is-hidden");

            window.setTimeout(function () {
                message.remove();
            }, 350);
        }, 5000);
    });
});


/* ===== Truck Delete Confirmation Modal ===== */

let truckDeleteTrigger = null;

function openTruckDeleteModal(button) {
    const modal = document.getElementById("truckDeleteModal");
    const form = document.getElementById("truckDeleteForm");
    const numberElement = document.getElementById("truckModalNumber");
    const confirmButton = document.getElementById("truckModalConfirm");

    if (!modal || !form || !numberElement || !confirmButton) {
        return;
    }

    truckDeleteTrigger = button;

    form.action = button.dataset.deleteUrl;
    numberElement.textContent = button.dataset.truckNumber;

    confirmButton.disabled = false;
    confirmButton.textContent = "Delete Truck";

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("truck-modal-open");

    confirmButton.focus();
}

function closeTruckDeleteModal() {
    const modal = document.getElementById("truckDeleteModal");

    if (!modal) {
        return;
    }

    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("truck-modal-open");

    if (truckDeleteTrigger) {
        truckDeleteTrigger.focus();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("truckDeleteModal");
    const form = document.getElementById("truckDeleteForm");
    const confirmButton = document.getElementById("truckModalConfirm");

    if (!modal || !form || !confirmButton) {
        return;
    }

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeTruckDeleteModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            modal.classList.contains("is-open")
        ) {
            closeTruckDeleteModal();
        }
    });

    form.addEventListener("submit", function () {
        if (!form.checkValidity()) {
            return;
        }

        confirmButton.disabled = true;
        confirmButton.textContent = "Deleting...";
    });
});
