
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("driverForm");
    const submitButton = document.getElementById("driverSubmitButton");

    if (!form || !submitButton) return;

    form.addEventListener("submit", function () {
        if (!form.checkValidity()) {
            return;
        }

        // Avoid repeated clicks while the form is submitting.
        if (form.dataset.submitting === "true") {
            return;
        }

        form.dataset.submitting = "true";
        submitButton.disabled = true;
        submitButton.textContent = "Saving...";
    });
});
