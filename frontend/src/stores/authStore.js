import { create } from 'zustand';
import apiClient from '../services/apiClient';

export const useAuthStore = create((set, get) => ({
    // State
    user: null,
    token: localStorage.getItem('token') || null,
    isLoading: false,
    error: null,

    // Actions
    login: async (username, password) => {
        set({ isLoading: true, error: null });

        try {
            // Call API to authenticate
            const response = await apiClient.auth.login(username, password);

            // Store token securely (using localStorage for MVP, consider HttpOnly cookies for production)
            const { access_token } = response.data;
            localStorage.setItem('token', access_token);

            // Update state with token
            set({ token: access_token, isLoading: false });

            // Fetch user data with token
            await get().loadUserFromToken();

            return true;
        } catch (error) {
            const errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
            set({ error: errorMessage, isLoading: false });
            return false;
        }
    },

    register: async (userData) => {
        set({ isLoading: true, error: null });

        try {
            // Call API to register
            await apiClient.auth.register(userData);
            set({ isLoading: false });

            // Login after successful registration
            return await get().login(userData.username, userData.password);
        } catch (error) {
            const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
            set({ error: errorMessage, isLoading: false });
            return false;
        }
    },

    logout: () => {
        // Clear token from storage
        localStorage.removeItem('token');

        // Reset state
        set({
            user: null,
            token: null,
            error: null
        });
    },

    loadUserFromToken: async () => {
        const token = get().token;

        // If no token, don't proceed
        if (!token) {
            return false;
        }

        set({ isLoading: true });

        try {
            // Call API to get user data
            const response = await apiClient.auth.me();

            // Update state with user data
            set({
                user: response.data,
                isLoading: false
            });

            return true;
        } catch (error) {
            // If token is invalid, logout
            if (error.response?.status === 401) {
                get().logout();
            }

            set({
                error: 'Failed to load user data',
                isLoading: false
            });

            return false;
        }
    },

    // Initialization - load user data on app start if token exists
    init: async () => {
        if (get().token) {
            await get().loadUserFromToken();
        }
    }
}));

// Initialize the store when it's imported
setTimeout(() => {
    useAuthStore.getState().init();
}, 0);
