
import ApiService from '../services/api.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('studentLoginForm');
    const loginButton = document.getElementById('loginButton');
    const errorMessage = document.getElementById('errorMessage');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        errorMessage.style.display = 'none';
        loginButton.disabled = true;
        loginButton.textContent = 'Signing in...';

        try {
            const response = await ApiService.login({
                username: username,
                password: password
            });

            const user = await ApiService.getCurrentUser();

            if (user.role !== 'student') {
                throw new Error('Access denied. Student credentials required.');
            }

            localStorage.setItem('userRole', user.role);
            localStorage.setItem('userData', JSON.stringify(user));

            window.location.href = 'dashboard.html';

        } catch (error) {
            errorMessage.textContent = error.message || 'Login failed. Please try again.';
            errorMessage.style.display = 'block';
            
            loginButton.disabled = false;
            loginButton.textContent = 'Sign In as Student';
        }
    });
});