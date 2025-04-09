import React from 'react';
import RegisterForm from '../features/auth/RegisterForm';

const RegisterPage = () => {
    return (
        <div className="auth-page">
            <h2>Create Your ThinkAlike Account</h2>
            <p>Join our community of like-minded individuals.</p>
            <RegisterForm />
        </div>
    );
};

export default RegisterPage;
