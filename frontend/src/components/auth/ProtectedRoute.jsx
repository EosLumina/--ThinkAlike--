import React, { useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

const ProtectedRoute = ({ children }) => {
    const { user, token, loadUserFromToken, isLoading } = useAuthStore();
    const location = useLocation();

    // Effect to load user data if we have a token but no user
    useEffect(() => {
        if (token && !user && !isLoading) {
            loadUserFromToken();
        }
    }, [token, user, loadUserFromToken, isLoading]);

    // Show loading indicator while checking authentication
    if (isLoading) {
        return <div className="loading-spinner">Loading...</div>;
    }

    // If not authenticated, redirect to login with return url
    if (!token) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    // If we have a token but no user data yet, show loading
    if (token && !user) {
        return <div className="loading-spinner">Loading user data...</div>;
    }

    // If authenticated and we have user data, render the protected content
    return children;
};

export default ProtectedRoute;
