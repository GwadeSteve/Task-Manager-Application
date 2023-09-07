// Function to validate password
function validatePassword() {
    var password1 = document.getElementById("id_password1").value;
    var otherFields = [document.querySelector('[name="first_name"]'), document.querySelector('[name="last_name"]'), document.querySelector('[name="email"]'), document.querySelector('[name="gender"]')];

    // Password validation logic here
    var passwordValid = (password1.length >= 8 && password1 !== otherFields.map(field => field.value).join(''));
    var passwordFeedback = document.querySelector('#id_password1 ~ .invalid-feedback');
    passwordFeedback.style.display = passwordValid ? 'none' : 'block';

    return passwordValid;
}

var emailField = document.querySelector("input[name='email']");
emailField.addEventListener("input", function() {
    if (!emailField.checkValidity()) {
        emailField.classList.add('is-invalid');
        emailField.classList.remove('is-valid');
    } else {
        emailField.classList.add('is-valid');
        emailField.classList.remove('is-invalid');
    }
});

// Event listener for input fields (show feedback as soon as user starts typing)
var inputFields = document.querySelectorAll(".form-control");
inputFields.forEach(function(field) {
    field.addEventListener("input", function() {
        if (!field.checkValidity()) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
        } else {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        }
    });
});

// Event listener for form submission
document.querySelector("form").addEventListener("submit", function(event) {
    // Check if all required fields are filled and passwords match
    var requiredFields = document.querySelectorAll("[required]");
    var valid = true;

    requiredFields.forEach(function(field) {
        if (!field.checkValidity()) {
            valid = false;
        }
    });

    if (!validatePassword() || !valid) {
        event.preventDefault(); // Prevent form submission
    }
});

// Event listener for email input field (show feedback as soon as user starts typing)
var emailField = document.querySelector("input[name='email']");
emailField.addEventListener("input", function() {
    if (!emailField.checkValidity()) {
        emailField.classList.add('is-invalid');
        emailField.classList.remove('is-valid');
    } else {
        emailField.classList.add('is-valid');
        emailField.classList.remove('is-invalid');
    }
});

// Event listener for form submission
document.querySelector("form").addEventListener("submit", function(event) {
    // Check if email field is valid
    var emailValid = emailField.checkValidity();
    var emailFeedback = document.querySelector('input[name="email"] ~ .invalid-feedback');
    emailFeedback.style.display = emailValid ? 'none' : 'block';

    if (!emailValid) {
        event.preventDefault(); // Prevent form submission if email is invalid
    }
});