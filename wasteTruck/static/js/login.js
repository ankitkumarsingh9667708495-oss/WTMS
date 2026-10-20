
const passwordField = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

if (passwordField && togglePassword) {
    togglePassword.addEventListener("click", function () {
        const isPasswordHidden = passwordField.type === "password";

        passwordField.type = isPasswordHidden ? "text" : "password";
        togglePassword.textContent = isPasswordHidden ? "Hide" : "Show";

        togglePassword.setAttribute(
            "aria-label",
            isPasswordHidden ? "Hide password" : "Show password"
        );

        togglePassword.setAttribute(
            "aria-pressed",
            String(isPasswordHidden)
        );
    });
}
