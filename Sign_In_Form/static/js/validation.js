function validateForm(){
    var name = document.forms.form.name.value;
    var regName = /\d+$/g;  

    var email = document.forms.form.email.value;
    // var regEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/g; 
    var regEmail = /\S+@\S+\.\S+/g;

    var phone = document.forms.form.phoneno.value;
    var regPhone = /^\d{10}$/;  

    var password = document.forms.form.password.value;
    var regPass = /^(\S)(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[~`!@#$%^&*()--+={}\[\]|\\:;"'<>,.?/_₹])[a-zA-Z0-9~`!@#$%^&*()--+={}\[\]|\\:;"'<>,.?/_₹]{10,16}$/;

    var country = document.forms.form.country_name.value;

    var state = document.forms.form.state_name.value;

    if (name == "" || regName.test(name)) {
        window.alert("Please enter your name properly.");
        name.focus();
        return false;
    }
      
    if (email == "" || !regEmail.test(email)) {
        window.alert("Please enter a valid e-mail address.");
        email.focus();
        return false;
    }
       
    if (password == "" || !regPass.test(password)) {
        alert("Please enter a valid password.");
        password.focus();
        return false;
    }

    if (phone == "" || !regPhone.test(phone)) {
        alert("Please enter valid phone number.");
        phone.focus();
        return false;
    }
  
    if (country.selectedIndex == -1) {
        alert("Please enter your country.");
        country.focus();
        return false;
    }

    if (state.selectedIndex == -1) {
        alert("Please enter your state.");
        state.focus();
        return false;
    }
  
    return true;
}