// js/utils/auth-guard.js
export function checkAuth(requiredRole = null) {
    const token = localStorage.getItem('authToken');
    const userRole = localStorage.getItem('userRole');

    if (!token) {
        window.location.href = '../pages/index.html';
        return false;
    }

    if (requiredRole && userRole !== requiredRole) {
        window.location.href = '../pages/index.html';
        return false;
    }

    return true;
}

export function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userData');
    window.location.href = '../pages/index.html';
}