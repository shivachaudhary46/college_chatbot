// js/auth/teacher-login.js
import ApiService from '../services/api.js';

history.pushState(null, "", location.href);
    window.onpopstate = function () {  
    window.location.href = "./index.html"; 
};
document.addEventListener('DOMContentLoaded', () => {
    console.log('Teacher login page loaded');
    
    const loginForm = document.getElementById('teacherLoginForm');
    const loginButton = document.getElementById('loginButton');
    const errorMessage = document.getElementById('errorMessage');

    if (!loginForm) {
        console.error('Login form not found!');
        return;
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted');
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        console.log('Attempting login with username:', username);

        errorMessage.style.display = 'none';
        loginButton.disabled = true;
        loginButton.textContent = 'Signing in...';

        try {
            // Step 1: Login
            console.log('Step 1: Calling login API...');
            const loginResponse = await ApiService.login({
                username: username,
                password: password
            });
            console.log('✓ Login response:', loginResponse);

            // Step 2: Get user details
            console.log('Step 2: Calling getCurrentUser API...');
            const user = await ApiService.getCurrentUser();
            console.log('✓ User data received:', user);

            // Step 3: Check role
            console.log('Step 3: Checking user role...');
            console.log('User role:', user.role);
            
            if (user.role !== 'teacher') {
                throw new Error(`Access denied. Expected 'teacher' role but got '${user.role}'`);
            }

            // Step 4: Store data
            console.log('Step 4: Storing user data...');
            localStorage.setItem('userRole', user.role);
            localStorage.setItem('userData', JSON.stringify(user));
            console.log('✓ Data stored in localStorage');

            // Step 5: Redirect
            console.log('Step 5: Redirecting to teacher portal...');
            window.location.href = 'teacher_portal.html';

        } catch (error) {
            console.error('❌ Login error:', error);
            console.error('Error message:', error.message);
            console.error('Error stack:', error.stack);
            
            errorMessage.textContent = error.message || 'Login failed. Please try again.';
            errorMessage.style.display = 'block';
            
            loginButton.disabled = false;
            loginButton.textContent = 'Sign In as Teacher';
        }
    });
});