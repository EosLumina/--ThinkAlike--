import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
    return (
        <div className="hero-section">
            <h1>Welcome to ThinkAlike</h1>
            <p className="lead">
                Connect with like-minded individuals based on shared values and interests.
            </p>
            <div className="cta-buttons">
                <Link to="/register" className="btn btn-primary">
                    Get Started
                </Link>
                <Link to="/login" className="btn btn-secondary">
                    Login
                </Link>
            </div>
        </div>
    );
};

export default HomePage;
