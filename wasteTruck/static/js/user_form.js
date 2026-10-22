// WTMS - User Registration Form

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("userRegistrationForm");
    const feedback = document.getElementById("formFeedback");

    if (!form) return;

    const submitButton = form.querySelector('button[type="submit"]');

    // Remove the error styling as the user corrects a field.
    form.querySelectorAll("input, select, textarea").forEach(function (field) {
        field.addEventListener("input", clearFieldError);
        field.addEventListener("change", clearFieldError);
    });

    function clearFieldError(event) {
        event.target.classList.remove("field-invalid");

        if (feedback) {
            feedback.textContent = "";
        }
    }

    form.addEventListener("submit", function (event) {
        let firstInvalidField = null;

        if (feedback) {
            feedback.textContent = "";
        }

        // Clear previous client-side error styling.
        form.querySelectorAll(".field-invalid").forEach(function (field) {
            field.classList.remove("field-invalid");
        });

        // Validate fields marked required by Django.
        const requiredFields = form.querySelectorAll(
            "input[required], select[required], textarea[required]"
        );

        requiredFields.forEach(function (field) {
            if (
                field.disabled ||
                field.type === "hidden" ||
                field.type === "checkbox" && !field.checked
            ) {
                if (field.type === "checkbox" && !field.checked) {
                    field.classList.add("field-invalid");
                    if (!firstInvalidField) firstInvalidField = field;
                }
                return;
            }

            if (!field.value.trim()) {
                field.classList.add("field-invalid");

                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });

        // Check password confirmation if both fields exist.
        const password1 = form.querySelector(
            'input[name="password1"]'
        );
        const password2 = form.querySelector(
            'input[name="password2"]'
        );

        if (
            password1 &&
            password2 &&
            password1.value &&
            password2.value &&
            password1.value !== password2.value
        ) {
            password2.classList.add("field-invalid");

            if (!firstInvalidField) {
                firstInvalidField = password2;
            }

            if (feedback) {
                feedback.textContent = "The passwords do not match.";
            }
        }

        if (firstInvalidField) {
            event.preventDefault();

            if (feedback && !feedback.textContent) {
                feedback.textContent =
                    "Please complete the required fields correctly.";
            }

            firstInvalidField.focus();
            return;
        }

        // Prevent accidental double-click submissions.
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Saving...";
        }
    });
});