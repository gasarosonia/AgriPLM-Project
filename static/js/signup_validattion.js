const signupForm = document.getElementById('signupForm'); // Assuming your form has an ID
signupForm.addEventListener('submit', function(event) {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;

  if (password !== confirmPassword) {
    event.preventDefault(); // Prevent form submission
    alert('Passwords do not match!');
  }
});