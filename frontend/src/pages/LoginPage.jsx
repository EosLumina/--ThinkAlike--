import React from 'react';
import LoginForm from '../features/auth/LoginForm';

const LoginPage = () => {
    return (
        <div className="auth-page">
            <h2>Login to ThinkAlike</h2>
            <p>Welcome back! Enter your credentials to access your account.</p>
            <LoginForm />
        </div>
    );
};

export default LoginPage;
