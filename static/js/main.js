document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('register-btn').addEventListener('click', function() {
        var registerForm = document.getElementById('register-form');
        if (registerForm.classList.contains('hidden')) {
            registerForm.classList.remove('hidden');
            registerForm.classList.add('show');
        } else {
            registerForm.classList.remove('show');
            registerForm.classList.add('hidden');
        }
    });

    document.getElementById('login-btn').addEventListener('click', function() {
        var name = document.getElementById('client-name').value;
        var phone = document.getElementById('client-phone').value;

        if (name === '' || phone === '') {
            alert('Пожалуйста, заполните все поля!');
            return;
        }    
        document.getElementById('register-form').classList.add('hidden');
        document.getElementById('pet-details').classList.remove('hidden');
    });

    var bootstrap = (typeof $().modal == 'function');
    console.log("Bootstrap загружен: ", bootstrap);
}); 