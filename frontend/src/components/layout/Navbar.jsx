import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

const Navbar = () => {
    const { user, logout } = useAuthStore();

    const handleLogout = () => {
        logout();
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    ThinkAlike
                </Link>

                <div className="nav-menu">
                    <NavLink to="/" className={({ isActive }) =>
                        isActive ? "nav-item active" : "nav-item"
                    }>
                        Home
                    </NavLink>

                    {user ? (
                        <>
                            <NavLink to="/dashboard" className={({ isActive }) =>
                                isActive ? "nav-item active" : "nav-item"
                            }>
                                Dashboard
                            </NavLink>

                            <NavLink to="/settings" className={({ isActive }) =>
                                isActive ? "nav-item active" : "nav-item"
                            }>
                                Settings
                            </NavLink>

                            <button onClick={handleLogout} className="nav-item btn-logout">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <NavLink to="/login" className={({ isActive }) =>
                                isActive ? "nav-item active" : "nav-item"
                            }>
                                Login
                            </NavLink>

                            <NavLink to="/register" className={({ isActive }) =>
                                isActive ? "nav-item active" : "nav-item"
                            }>
                                Register
                            </NavLink>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
