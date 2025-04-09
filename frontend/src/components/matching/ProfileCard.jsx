import React from 'react';
import './ProfileCard.css';

/**
 * ProfileCard component displays a user profile with compatibility information
 * Implements UI-driven validation through visual indicators
 */
const ProfileCard = ({ profile, compatibilityScore, sharedValues }) => {
    // Calculate score color based on compatibility
    const getScoreColor = (score) => {
        if (score >= 0.8) return 'high-match';
        if (score >= 0.6) return 'good-match';
        if (score >= 0.4) return 'moderate-match';
        return 'low-match';
    };

    return (
        <div className="profile-card">
            <div className="profile-header">
                <div className="profile-image">
                    {profile.profilePictureUrl ? (
                        <img src={profile.profilePictureUrl} alt={profile.username} />
                    ) : (
                        <div className="profile-image-placeholder">
                            {profile.fullName.substring(0, 1)}
                        </div>
                    )}
                </div>
                <div className="profile-info">
                    <h3>{profile.fullName}</h3>
                    <p className="username">@{profile.username}</p>
                    {profile.location && <p className="location">{profile.location}</p>}
                </div>
                <div className={`compatibility-score ${getScoreColor(compatibilityScore)}`}>
                    <span className="score-value">{Math.round(compatibilityScore * 100)}%</span>
                    <span className="score-label">Match</span>
                </div>
            </div>

            <div className="profile-content">
                {profile.bio && <p className="bio">{profile.bio}</p>}

                {sharedValues.length > 0 && (
                    <div className="shared-values">
                        <h4>Shared Values</h4>
                        <div className="value-tags">
                            {sharedValues.map((value, index) => (
                                <span key={index} className="value-tag">{value}</span>
                            ))}
                        </div>
                    </div>
                )}

                <div className="profile-actions">
                    <button className="connect-button">Connect</button>
                    <button className="view-profile-button">View Full Profile</button>
                </div>
            </div>
        </div>
    );
};

export default ProfileCard;
