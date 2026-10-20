
const toggleButtons = document.querySelectorAll(".toggle-password");

toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
        const targetId = this.dataset.target;
        const passwordField = document.getElementById(targetId);

        if (!passwordField) return;

        const isHidden = passwordField.type === "password";

        passwordField.type = isHidden ? "text" : "password";
        this.textContent = isHidden ? "Hide" : "Show";

        this.setAttribute(
            "aria-label",
            isHidden ? "Hide password" : "Show password"
        );

        this.setAttribute("aria-pressed", String(isHidden));
    });
});
