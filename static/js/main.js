document.addEventListener("DOMContentLoaded", function () {
  // Function to set cookie with proper attributes
  function setCookie(name, value, days) {
    let expires = "";
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie =
      name + "=" + (value || "") + expires + "; path=/; SameSite=Lax; Secure";
  }

  // Function to get cookie
  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === " ") c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  document
    .getElementById("register-btn")
    .addEventListener("click", function () {
      var registerForm = document.getElementById("register-form");
      if (registerForm.classList.contains("hidden")) {
        registerForm.classList.remove("hidden");
        registerForm.classList.add("show");
      } else {
        registerForm.classList.remove("show");
        registerForm.classList.add("hidden");
      }
    });

  document.getElementById("login-btn").addEventListener("click", function () {
    var name = document.getElementById("client-name").value;
    var phone = document.getElementById("client-phone").value;

    if (name === "" || phone === "") {
      alert("Пожалуйста, заполните все поля!");
      return;
    }

    // Store user data in cookie
    setCookie("userData", JSON.stringify({name, phone}), 1);

    document.getElementById("register-form").classList.add("hidden");
    document.getElementById("pet-details").classList.remove("hidden");
  });

  // Check for existing user data on page load
  const userData = getCookie("userData");
  if (userData) {
    const data = JSON.parse(userData);
    document.getElementById("client-name").value = data.name;
    document.getElementById("client-phone").value = data.phone;
  }

  var bootstrap = typeof $().modal == "function";
  console.log("Bootstrap загружен: ", bootstrap);
});
