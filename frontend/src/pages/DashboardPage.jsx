import React from 'react';

const DashboardPage = () => {
    return (
        <div className="dashboard-page">
            <h2>My Dashboard</h2>
            <p>Welcome to your personal ThinkAlike dashboard.</p>

            <div className="dashboard-content">
                <div className="dashboard-card">
                    <h3>My Profile</h3>
                    <p>Update your personal information and preferences.</p>
                </div>

                <div className="dashboard-card">
                    <h3>Connections</h3>
                    <p>View and manage your connections.</p>
                </div>

                <div className="dashboard-card">
                    <h3>Recent Activity</h3>
                    <p>See your recent interactions on the platform.</p>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
