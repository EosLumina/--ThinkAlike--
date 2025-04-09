import axios from 'axios';

// Get API URL from environment variables, with fallback for local development
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API_V1 = `${API_URL}/api/v1`;

// Create axios instance
const axiosInstance = axios.create({
    baseURL: API_V1,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token to requests
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');

        // If token exists, add to Authorization header
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle 401 Unauthorized errors consistently
        if (error.response && error.response.status === 401) {
            // If we have a localStorage implementation of token storage:
            localStorage.removeItem('token');

            // Redirect to login page if needed
            // If using React Router v6, we'd handle this in a component
        }

        return Promise.reject(error);
    }
);

// API endpoints
const apiClient = {
    // Authentication endpoints
    auth: {
        // Login endpoint
        login: (username, password) => {
            // Format data for OAuth2 password flow
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            return axios.post(`${API_V1}/auth/token`, formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
        },

        // Register endpoint
        register: (userData) => {
            return axiosInstance.post(`/auth/register`, userData);
        },

        // Get current user endpoint
        me: () => {
            return axiosInstance.get(`/auth/me`);
        },
    },

    // User profile endpoints
    profile: {
        // Get user profile
        get: () => {
            return axiosInstance.get(`/users/me/profile`);
        },

        // Update user profile
        update: (profileData) => {
            return axiosInstance.put(`/users/me/profile`, profileData);
        },
    },

    // Add more API endpoints here as needed
};

export default apiClient;
