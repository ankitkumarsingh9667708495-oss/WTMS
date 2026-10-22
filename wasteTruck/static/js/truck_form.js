
/* ===== Truck Form Submission ===== */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("truckForm");
    const submitButton = document.getElementById("truckSubmitButton");

    if (!form || !submitButton) return;

    form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
            return;
        }

        if (form.dataset.submitting === "true") {
            event.preventDefault();
            return;
        }

        form.dataset.submitting = "true";
        submitButton.disabled = true;
        submitButton.textContent = "Saving...";
    });
});
