//hide and show change icon and show and hide password
let password = document.getElementById("password");
let icon = document.querySelector("#iconlock");

function showHidePassword() {
  if (password.type === "password") {
    password.type = "text";
    icon.className = "fas fa-eye-slash";
  } else {
    password.type = "password";
    icon.className = "fas fa-eye";
  }
}

icon.addEventListener("click", showHidePassword);

let password2 = document.getElementById("password2");
let icon2 = document.querySelector("#iconlock2");

function showHidePassword2() {
  if (password2.type === "password") {
    password2.type = "text";
    icon2.className = "fas fa-eye-slash";
  } else {
    password2.type = "password";
    icon2.className = "fas fa-eye";
  }
}

icon2.addEventListener("click", showHidePassword2);

let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
let userInput = document.getElementById("Email");
let login = document.getElementById("Logain");

login.onclick = function() {
  if (!emailPattern.test(userInput.value)) {
    Swal.fire({
      icon: 'error',
      title: 'Something in your input is wrong',
      text: 'Please correct and try again',
      
    });
  } 
  }
let emailPattern2 = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
let userInput2 = document.getElementById("Email2");
let Register = document.getElementById("Register");

Register.onclick = function() {
  if (!emailPattern2.test(userInput2.value)) {
    Swal.fire({
      icon: 'error',
      title: 'Something in your input is wrong',
      text: 'Please correct and try again',
      
    });
  } 
};