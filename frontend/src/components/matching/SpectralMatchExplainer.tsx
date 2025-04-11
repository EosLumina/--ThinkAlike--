import React from 'react';
import { ValueProfile, OrbitRelationship } from '../../types/valueTypes';
import { DataTraceability } from '../transparency/DataTraceability';

interface SpectralMatchExplainerProps {
  userProfile: ValueProfile;
  matchProfile: ValueProfile;
  relationship: OrbitRelationship;
  matchingData: Record<string, any>; // Transparent algorithm data
}

const SpectralMatchExplainer: React.FC<SpectralMatchExplainerProps> = ({
  userProfile,
  matchProfile,
  relationship,
  matchingData
}) => {
  // Component implementation to visualize:
  // 1. Value spectra comparison
  // 2. Matching algorithm transparency
  // 3. User controls for tuning matching preferences

  return (
    <div className="spectral-match-explainer">
      <h3>Connection Insight: {matchProfile.userId}</h3>

      {/* Value Spectra Visualization */}
      <SpectralComparisonChart
        userProfile={userProfile}
        matchProfile={matchProfile}
      />

      {/* Relationship Quality Section */}
      <RelationshipQualitySection relationship={relationship} />

      {/* Algorithm Transparency */}
      <DataTraceability
        context={{
          type: "VALUE_MATCHING",
          primaryId: userProfile.userId,
          secondaryId: matchProfile.userId
        }}
        data={matchingData}
      />

      {/* User Controls for Match Preferences */}
      <MatchPreferencesControls
        userProfile={userProfile}
        onPreferencesChange={/* handler */}
      />
    </div>
  );
};
