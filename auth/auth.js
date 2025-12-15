// ============================================
// TAB SWITCHING
// ============================================
const tabs = document.querySelectorAll('.tab');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;
        switchTab(targetTab);
    });
});

document.querySelectorAll('.switch-tab').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetTab = link.dataset.target;
        switchTab(targetTab);
    });
});

function switchTab(tabName) {
    // Update tab buttons
    tabs.forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update form visibility
    if (tabName === 'login') {
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
    } else {
        signupForm.classList.add('active');
        loginForm.classList.remove('active');
    }

    // Clear error messages
    clearMessages();
}

function clearMessages() {
    document.querySelectorAll('.error-message, .success-message').forEach(msg => {
        msg.classList.remove('show');
        msg.textContent = '';
    });
}

// ============================================
// LOGIN HANDLER
// ============================================
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    clearMessages();

    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });

        if (error) throw error;

        // Store session token
        sessionStorage.setItem('auth_token', data.session.access_token);
        sessionStorage.setItem('user_email', data.user.email);
        sessionStorage.setItem('user_id', data.user.id);

        // Redirect to Streamlit app
        window.location.href = 'http://localhost:8501';

    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
});

// ============================================
// SIGNUP HANDLER
// ============================================
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const errorDiv = document.getElementById('signup-error');
    const successDiv = document.getElementById('signup-success');

    clearMessages();

    if (password.length < 6) {
        errorDiv.textContent = 'Password must be at least 6 characters';
        errorDiv.classList.add('show');
        return;
    }

    try {
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password
        });

        if (error) throw error;

        successDiv.textContent = '✅ Account created! Please switch to Login tab.';
        successDiv.classList.add('show');

        // Clear form
        document.getElementById('signup-email').value = '';
        document.getElementById('signup-password').value = '';

        // Auto-switch to login after 2 seconds
        setTimeout(() => {
            switchTab('login');
        }, 2000);

    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
});

// ============================================
// CHECK IF ALREADY LOGGED IN
// ============================================
window.addEventListener('load', async () => {
    const { data: { session } } = await supabase.auth.getSession();

    if (session) {
        // Already logged in, redirect to Streamlit
        sessionStorage.setItem('auth_token', session.access_token);
        sessionStorage.setItem('user_email', session.user.email);
        sessionStorage.setItem('user_id', session.user.id);
        window.location.href = 'http://localhost:8501';
    }
});
