function validateForm() {
    var enterprisename = document.getElementById('enterprisename').value.trim();
    var username = document.getElementById('username').value.trim();
    var password = document.getElementById('password').value.trim();
    var email = document.getElementById('email').value.trim();
    var mobile = document.getElementById('mobile').value.trim();
    var file = document.getElementById('formFileLg').value.trim();

    var enterprisenameError = document.getElementById('enterprisenameError');
    var usernameError = document.getElementById('usernameError');
    var passwordError = document.getElementById('passwordError');
    var emailError = document.getElementById('emailError');
    var mobileError = document.getElementById('mobileError');
    var fileError = document.getElementById('fileError');

    var isValid = true;

    // Regular expressions for validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var mobileRegex = /^\d{10}$/;

    if (enterprisename === '') {
        enterprisenameError.innerText = 'Please enter enterprise name';
        isValid = false;
    } else {
        enterprisenameError.innerText = '';
    }

    if (username === '') {
        usernameError.innerText = 'Please enter username';
        isValid = false;
    } else {
        usernameError.innerText = '';
    }

    if (password === '') {
        passwordError.innerText = 'Please enter password';
        isValid = false;
    } else {
        passwordError.innerText = '';
    }

    if (email === '') {
        emailError.innerText = 'Please enter email';
        isValid = false;
    } else if (!emailRegex.test(email)) {
        emailError.innerText = 'Please enter a valid email address';
        isValid = false;
    } else {
        emailError.innerText = '';
    }

    if (mobile === '') {
        mobileError.innerText = 'Please enter mobile number';
        isValid = false;
    } else if (!mobileRegex.test(mobile)) {
        mobileError.innerText = 'Please enter a valid 10-digit mobile number';
        isValid = false;
    } else {
        mobileError.innerText = '';
    }

    if (file === '') {
        fileError.innerText = 'Please upload logo';
        isValid = false;
    } else {
        var allowedExtensions = ['jpg', 'jpeg', 'png'];
        var fileExtension = file.name.split('.').pop().toLowerCase();
    
        if (allowedExtensions.indexOf(fileExtension) === -1) {
            fileError.innerText = 'Only JPG and PNG files are allowed';
            isValid = false;
        } else {
            fileError.innerText = '';
        }
    }
    
    return isValid;
}

