#!/usr/bin/env python3
"""
Frontend Guardian: ThinkAlike Frontend Development Guide
-------------------------------------------------------
A specialized AI guide focused on frontend development within ThinkAlike.
This guide helps contributors understand the frontend architecture,
React component patterns, state management, and UI/UX principles that
align with ThinkAlike's ethical vision of user sovereignty.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Define root project directory
PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent.parent.parent

# Frontend-specific resources
FRONTEND_RESOURCES = {
    "component_patterns": [
        {
            "name": "Sovereign Data Component",
            "description": "Components that give users full control over their data",
            "example": "DataTraceabilityCard, ConsentToggle, PrivacyDisplay",
            "pattern": """
import React, { useState } from 'react';
import { useUserConsent } from '../../hooks/useUserConsent';
import { DataTraceability } from '../ui/DataTraceability';

export const SovereignDataComponent = ({ data, onUpdate }) => {
  const { consent, updateConsent } = useUserConsent(data.type);
  const [isVisible, setIsVisible] = useState(true);
  
  // Users can toggle visibility of their data
  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };
  
  return (
    <div className="sovereign-data-container">
      <header className="data-control-header">
        <h3>{data.title}</h3>
        <div className="control-buttons">
          <button onClick={toggleVisibility}>
            {isVisible ? 'Hide Data' : 'Show Data'}
          </button>
          <ConsentToggle
            isActive={consent.isActive}
            onChange={(value) => updateConsent({ ...consent, isActive: value })}
          />
        </div>
      </header>
      
      {isVisible && consent.isActive && (
        <div className="data-content">
          {data.content}
          <DataTraceability source={data.source} />
        </div>
      )}
    </div>
  );
};
"""
        },
        {
            "name": "Transparent Process Component",
            "description": "Components that explain how data is being processed",
            "example": "AlgorithmExplainer, ProcessVisualizer, MatchingLogic",
            "pattern": """
import React from 'react';
import { ProcessSteps } from '../visualization/ProcessSteps';
import { CodeDisplay } from '../ui/CodeDisplay';

export const TransparentProcessComponent = ({ process }) => {
  return (
    <div className="transparent-process">
      <h3>{process.name}</h3>
      <p className="process-description">{process.description}</p>
      
      <div className="process-visualization">
        <ProcessSteps steps={process.steps} />
      </div>
      
      <details className="code-details">
        <summary>See How This Works</summary>
        <CodeDisplay 
          code={process.pseudoCode} 
          language="javascript" 
        />
        <p className="ethical-notes">{process.ethicalConsiderations}</p>
      </details>
    </div>
  );
};
"""
        }
    ],
    "state_management": [
        {
            "name": "Ethical State Management",
            "description": "Patterns for managing state that respect user sovereignty",
            "principles": [
                "Local-first: Prioritize local state over server state when possible",
                "Transparent: Make state changes visible to users",
                "Consent-based: Only sync data with explicit permission",
                "Recoverable: Allow users to revert state changes"
            ]
        }
    ],
    "learning_resources": [
        {
            "topic": "React Basics",
            "for_beginners": True,
            "resources": [
                {"title": "Official React Tutorial", "url": "https://reactjs.org/tutorial/tutorial.html"},
                {"title": "React for Beginners", "url": "https://reactforbeginners.com/"}
            ]
        },
        {
            "topic": "TypeScript with React",
            "for_beginners": False,
            "resources": [
                {"title": "React TypeScript Cheatsheet", "url": "https://github.com/typescript-cheatsheets/react"}
            ]
        }
    ]
}

class FrontendGuardian:
    """
    The Frontend Guardian guide specializes in helping contributors
    understand and contribute to ThinkAlike's frontend systems.
    """
    
    def __init__(self):
        """Initialize the Frontend Guardian guide."""
        self.guide_dir = PROJECT_ROOT / "tools" / "ai_guides"
        self.resources = FRONTEND_RESOURCES
        self.frontend_path = PROJECT_ROOT / "frontend"
        self.project_structure = self._analyze_frontend_structure()
        
    def _analyze_frontend_structure(self) -> Dict:
        """Analyze the current frontend project structure."""
        if not self.frontend_path.exists():
            return {"error": "Frontend directory not found"}
        
        structure = {
            "components": [],
            "pages": [],
            "hooks": [],
            "utils": [],
            "styles": []
        }
        
        # Map directories to structure keys
        dir_mapping = {
            "components": "components",
            "pages": "pages",
            "hooks": "hooks",
            "utils": "utils",
            "styles": "styles",
            "src/components": "components",
            "src/pages": "pages",
            "src/hooks": "hooks",
            "src/utils": "utils",
            "src/styles": "styles"
        }
        
        # Scan for TypeScript/JavaScript files in relevant directories
        for rel_dir, struct_key in dir_mapping.items():
            dir_path = self.frontend_path / rel_dir
            if dir_path.exists():
                for file_path in dir_path.glob("**/*.{ts,tsx,js,jsx}"):
                    structure[struct_key].append(str(file_path.relative_to(self.frontend_path)))
        
        return structure
    
    def get_project_overview(self) -> str:
        """Get an overview of the current frontend project structure."""
        structure = self._analyze_frontend_structure()
        
        if "error" in structure:
            return f"⚠️ {structure['error']}\n\nIt seems the frontend project hasn't been set up yet. I can guide you through setting it up if you'd like."
        
        # Count files by type
        component_count = len(structure["components"])
        page_count = len(structure["pages"])
        hook_count = len(structure["hooks"])
        util_count = len(structure["utils"])
        
        overview = f"""
# ThinkAlike Frontend Overview

## Project Structure
The frontend project currently contains:
- {component_count} components
- {page_count} pages
- {hook_count} custom hooks
- {util_count} utility files

## Key Components
"""
        
        # Add some example components if they exist
        if structure["components"]:
            overview += "Some important components in the project:\n"
            for component in structure["components"][:5]:  # Show up to 5 components
                overview += f"- `{component}`\n"
        else:
            overview += "No components found yet. I can help you create your first component!\n"
            
        # Add tech stack info
        package_json = self.frontend_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    pkg_data = json.load(f)
                dependencies = pkg_data.get("dependencies", {})
                
                overview += "\n## Technology Stack\n"
                if "react" in dependencies:
                    overview += f"- React {dependencies['react']}\n"
                if "typescript" in dependencies or "typescript" in pkg_data.get("devDependencies", {}):
                    overview += "- TypeScript\n"
                # Add other relevant dependencies
                for key in ["react-router", "redux", "mobx", "chakra-ui", "material-ui", "@mui/material"]:
                    if key in dependencies:
                        overview += f"- {key} {dependencies[key]}\n"
            except:
                overview += "\nUnable to parse package.json for tech stack information.\n"
        
        return overview
    
    def suggest_first_contribution(self, experience_level: str = "beginner") -> str:
        """Suggest a first contribution based on experience level."""
        structure = self._analyze_frontend_structure()
        
        if "error" in structure:
            return """
## Setting Up the Frontend Project

For your first contribution, let's set up the basic frontend project structure:

1. Create the frontend directory:
   ```bash
   mkdir -p frontend/src/components frontend/src/pages frontend/src/hooks frontend/src/utils frontend/src/styles
   ```

2. Initialize a React project with TypeScript:
   ```bash
   cd frontend
   npm init -y
   npm install react react-dom
   npm install --save-dev typescript @types/react @types/react-dom
   ```

3. Create a basic tsconfig.json:
   ```bash
   echo '{
     "compilerOptions": {
       "target": "es5",
       "lib": ["dom", "dom.iterable", "esnext"],
       "allowJs": true,
       "skipLibCheck": true,
       "esModuleInterop": true,
       "allowSyntheticDefaultImports": true,
       "strict": true,
       "forceConsistentCasingInFileNames": true,
       "noFallthroughCasesInSwitch": true,
       "module": "esnext",
       "moduleResolution": "node",
       "resolveJsonModule": true,
       "isolatedModules": true,
       "noEmit": true,
       "jsx": "react-jsx"
     },
     "include": ["src"]
   }' > tsconfig.json
   ```

This will give you a solid foundation to start building ThinkAlike's frontend!
"""
        
        if experience_level == "beginner":
            return """
## Your First Frontend Contribution

As a beginner, here's a perfect first contribution:

### Create a User Sovereignty Component

This component will show users what data is being stored and give them control over it - a core principle of ThinkAlike.

1. Create a new file at `frontend/src/components/ui/DataVisibilityToggle.tsx`:

```tsx
import React, { useState } from 'react';

interface DataVisibilityToggleProps {
  dataType: string;
  description: string;
  initiallyVisible?: boolean;
  onToggle?: (isVisible: boolean) => void;
}

/**
 * A component that gives users control over the visibility of their data,
 * embodying ThinkAlike's principle of user sovereignty.
 */
export const DataVisibilityToggle: React.FC<DataVisibilityToggleProps> = ({
  dataType,
  description,
  initiallyVisible = true,
  onToggle
}) => {
  const [isVisible, setIsVisible] = useState(initiallyVisible);
  
  const handleToggle = () => {
    const newVisibility = !isVisible;
    setIsVisible(newVisibility);
    if (onToggle) {
      onToggle(newVisibility);
    }
  };
  
  return (
    <div className="data-visibility-control">
      <div className="data-info">
        <h4>{dataType}</h4>
        <p>{description}</p>
      </div>
      <button 
        className={`visibility-toggle ${isVisible ? 'visible' : 'hidden'}`}
        onClick={handleToggle}
      >
        {isVisible ? 'Hide Data' : 'Show Data'}
      </button>
    </div>
  );
};
```

2. Create a simple test to ensure it works:

```tsx
// frontend/src/components/ui/DataVisibilityToggle.test.tsx
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { DataVisibilityToggle } from './DataVisibilityToggle';

describe('DataVisibilityToggle', () => {
  test('renders with initial state', () => {
    render(
      <DataVisibilityToggle 
        dataType="Location History" 
        description="Your stored location data" 
      />
    );
    
    expect(screen.getByText('Location History')).toBeInTheDocument();
    expect(screen.getByText('Your stored location data')).toBeInTheDocument();
    expect(screen.getByText('Hide Data')).toBeInTheDocument();
  });
  
  test('toggles visibility when clicked', () => {
    const mockToggle = jest.fn();
    render(
      <DataVisibilityToggle 
        dataType="Location History" 
        description="Your stored location data"
        onToggle={mockToggle}
      />
    );
    
    // Initially visible
    const button = screen.getByText('Hide Data');
    
    // Click to hide
    fireEvent.click(button);
    expect(screen.getByText('Show Data')).toBeInTheDocument();
    expect(mockToggle).toHaveBeenCalledWith(false);
    
    // Click to show again
    fireEvent.click(screen.getByText('Show Data'));
    expect(screen.getByText('Hide Data')).toBeInTheDocument();
    expect(mockToggle).toHaveBeenCalledWith(true);
  });
});
```

This component embodies ThinkAlike's commitment to user sovereignty and transparency, giving users control over their data visibility.
"""
        else:  # experienced developer
            return """
## Your First Frontend Contribution

For an experienced developer, here's a meaningful first contribution:

### Create a Value-Based Matching Component

This component will implement ThinkAlike's ethical matching interface, showing why matches are suggested and giving users transparency and control.

1. Create a new file at `frontend/src/components/matching/ValueMatchCard.tsx`:

```tsx
import React, { useState } from 'react';
import { MatchSimilarity } from './MatchSimilarity';
import { ValueTag } from '../ui/ValueTag';
import { DataTraceability } from '../ui/DataTraceability';

interface ValueMatchCardProps {
  match: {
    id: string;
    name: string;
    profileImage?: string;
    matchPercentage: number;
    sharedValues: Array<{
      name: string;
      score: number;
      description: string;
    }>;
    matchReasoning: string;
    dataSource: {
      features: string[];
      algorithm: string;
      lastUpdated: string;
    };
  };
  onAccept: (id: string) => void;
  onDecline: (id: string) => void;
  onRequestMoreInfo: (id: string) => void;
}

/**
 * A component that displays potential matches with transparency about
 * the matching process, aligning with ThinkAlike's ethical principles.
 */
export const ValueMatchCard: React.FC<ValueMatchCardProps> = ({
  match,
  onAccept,
  onDecline,
  onRequestMoreInfo
}) => {
  const [showDetails, setShowDetails] = useState(false);
  
  return (
    <div className="value-match-card">
      <div className="match-header">
        <img 
          src={match.profileImage || '/default-avatar.png'} 
          alt={`${match.name}'s profile`} 
          className="profile-image"
        />
        <div className="match-info">
          <h3>{match.name}</h3>
          <MatchSimilarity percentage={match.matchPercentage} />
        </div>
      </div>
      
      <div className="shared-values">
        <h4>Shared Values</h4>
        <div className="value-tags">
          {match.sharedValues.map(value => (
            <ValueTag 
              key={value.name}
              name={value.name}
              score={value.score}
              description={value.description}
            />
          ))}
        </div>
      </div>
      
      <button 
        className="details-toggle"
        onClick={() => setShowDetails(!showDetails)}
      >
        {showDetails ? 'Hide Match Details' : 'Show Match Details'}
      </button>
      
      {showDetails && (
        <div className="match-details">
          <p className="match-reasoning">{match.matchReasoning}</p>
          
          <DataTraceability 
            features={match.dataSource.features}
            algorithm={match.dataSource.algorithm}
            lastUpdated={match.dataSource.lastUpdated}
          />
        </div>
      )}
      
      <div className="match-actions">
        <button 
          className="action-decline"
          onClick={() => onDecline(match.id)}
        >
          Decline
        </button>
        <button 
          className="action-more-info"
          onClick={() => onRequestMoreInfo(match.id)}
        >
          More Info
        </button>
        <button 
          className="action-accept"
          onClick={() => onAccept(match.id)}
        >
          Accept
        </button>
      </div>
    </div>
  );
};
```

2. Create the supporting components:

```tsx
// frontend/src/components/matching/MatchSimilarity.tsx
import React from 'react';

interface MatchSimilarityProps {
  percentage: number;
}

export const MatchSimilarity: React.FC<MatchSimilarityProps> = ({ percentage }) => {
  // Color gradient from yellow (50%) to green (100%)
  const color = percentage < 75 
    ? `rgb(255, ${Math.floor(255 * (percentage - 50) / 25)}, 0)` 
    : `rgb(${Math.floor(255 * (100 - percentage) / 25)}, 255, 0)`;
  
  return (
    <div className="match-similarity">
      <div className="percentage-display" style={{ color }}>
        {percentage}% Match
      </div>
      <div className="percentage-bar">
        <div 
          className="percentage-fill" 
          style={{ width: `${percentage}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
};
```

```tsx
// frontend/src/components/ui/ValueTag.tsx
import React, { useState } from 'react';

interface ValueTagProps {
  name: string;
  score: number;
  description: string;
}

export const ValueTag: React.FC<ValueTagProps> = ({ name, score, description }) => {
  const [showDescription, setShowDescription] = useState(false);
  
  return (
    <div 
      className="value-tag"
      onMouseEnter={() => setShowDescription(true)}
      onMouseLeave={() => setShowDescription(false)}
    >
      <span className="value-name">{name}</span>
      <span className="value-score">{score}</span>
      
      {showDescription && (
        <div className="value-description-popup">
          {description}
        </div>
      )}
    </div>
  );
};
```

```tsx
// frontend/src/components/ui/DataTraceability.tsx
import React, { useState } from 'react';

interface DataTraceabilityProps {
  features: string[];
  algorithm: string;
  lastUpdated: string;
}

export const DataTraceability: React.FC<DataTraceabilityProps> = ({
  features,
  algorithm,
  lastUpdated
}) => {
  const [expanded, setExpanded] = useState(false);
  
  return (
    <div className="data-traceability">
      <button 
        className="traceability-toggle"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? 'Hide Data Source' : 'Show Data Source'}
      </button>
      
      {expanded && (
        <div className="traceability-details">
          <p className="algorithm-name">
            <strong>Matching Algorithm:</strong> {algorithm}
          </p>
          <p className="last-updated">
            <strong>Last Updated:</strong> {lastUpdated}
          </p>
          <div className="data-features">
            <strong>Based On:</strong>
            <ul>
              {features.map(feature => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
          </div>
          <p className="data-ethics-note">
            All matching data is processed locally in your browser and only shared with your explicit consent.
          </p>
        </div>
      )}
    </div>
  );
};
```

This implementation showcases ThinkAlike's commitment to transparency in algorithms, user sovereignty over matching, and ethical data handling - all core principles of the platform.
"""
    
    def explain_frontend_concept(self, concept: str) -> str:
        """Explain a frontend concept in the context of ThinkAlike."""
        # Concept explanations indexed by keywords
        concepts = {
            "component": """
# Components in ThinkAlike

In ThinkAlike's frontend architecture, components aren't just UI building blocks - they're embodiments of our ethical principles.

## Core Component Types

### Sovereign Data Components
These components give users complete visibility and control over their data. Examples:
- `DataTraceabilityCard`: Shows where data came from and how it's being used
- `ConsentToggle`: Explicit permission controls for data usage
- `PrivacyDisplay`: Visualization of privacy settings and implications

### Transparent Process Components
These components make algorithmic processes visible and understandable:
- `AlgorithmExplainer`: Visual breakdown of matching algorithms
- `ProcessVisualizer`: Step-by-step visualization of data flows
- `MatchingLogic`: Shows exactly why a match was suggested

### Value-Based UI Components
These components embody ThinkAlike's core ethical values:
- `ValueAlignment`: Shows alignment between user values and community
- `EthicalConsiderations`: Highlights ethical implications of actions
- `CommonGoodMetric`: Visualizes collective benefit of individual choices

## Component Design Principles

1. **User Sovereignty**: Every component touching user data must provide visibility and control
2. **Radical Transparency**: No black boxes - processes must be explainable
3. **Minimal Data**: Components should minimize data requirements and storage
4. **Accessibility First**: Design for universal access across abilities and devices
5. **Local-First Processing**: Prefer client-side processing when possible for privacy

## Component Implementation

In code, ThinkAlike components follow these patterns:
- Clear, ethical docstrings explaining purpose and principles
- Explicit consent handling for data-related operations
- Transparency props for revealing underlying processes
- Accessibility built in from the start, not added later
""",
            "state": """
# State Management in ThinkAlike

State management in ThinkAlike goes beyond typical frontend concerns - it's a philosophical stance on data ownership and sovereignty.

## Ethical State Management Principles

1. **Local-First**: User data belongs to users first, with server state as an optional sync target
2. **Transparent Changes**: State mutations are always visible and explained to users
3. **Consent-Based Sync**: Data only moves from local to server state with explicit permission
4. **Recoverable History**: Users can view state history and recover previous states
5. **Minimal Footprint**: Only store what's necessary, with clear data lifecycle policies

## Implementation Patterns

### Sovereign User State Pattern
```tsx
export function useSovereignState<T>(
  initialState: T,
  options: {
    persistKey?: string;
    syncToServer?: boolean;
    syncConsentKey?: string;
    encryptLocally?: boolean;
  }
) {
  // Local state always exists
  const [localState, setLocalState] = useState(
    // Try to load from localStorage if persistKey provided
    options.persistKey
      ? JSON.parse(localStorage.getItem(options.persistKey) || 'null') || initialState
      : initialState
  );
  
  // Consent state for server sync
  const [syncConsent, setSyncConsent] = useState(
    options.syncConsentKey
      ? localStorage.getItem(options.syncConsentKey) === 'true'
      : false
  );
  
  // State history for recoverability
  const [stateHistory, setStateHistory] = useState<T[]>([localState]);
  
  // Update function that maintains history
  const updateState = (newState: T) => {
    setLocalState(newState);
    setStateHistory([...stateHistory, newState]);
    
    // Persist locally if requested
    if (options.persistKey) {
      localStorage.setItem(
        options.persistKey,
        JSON.stringify(options.encryptLocally ? encrypt(newState) : newState)
      );
    }
    
    // Sync to server if consent given
    if (options.syncToServer && syncConsent) {
      syncStateToServer(newState);
    }
  };
  
  // Toggle server sync consent
  const toggleSyncConsent = (value: boolean) => {
    setSyncConsent(value);
    if (options.syncConsentKey) {
      localStorage.setItem(options.syncConsentKey, value.toString());
    }
  };
  
  // Recover previous state
  const recoverPreviousState = () => {
    if (stateHistory.length > 1) {
      const previousState = stateHistory[stateHistory.length - 2];
      setLocalState(previousState);
      setStateHistory(stateHistory.slice(0, -1));
    }
  };
  
  return {
    state: localState,
    updateState,
    syncConsent,
    toggleSyncConsent,
    stateHistory,
    recoverPreviousState,
  };
}
```

This pattern ensures:
- Data is always available locally
- Users explicitly consent to server syncing
- History is maintained for recovery
- Data can be encrypted locally for sensitive information
""",
            "typescript": """
# TypeScript in ThinkAlike

TypeScript isn't just a tool for catching bugs in ThinkAlike - it's a way to encode our ethical principles into the type system itself.

## Ethical TypeScript Patterns

### Consent Types
```typescript
// Require explicit consent for operations
type ConsentType = 'data_storage' | 'matching' | 'location_sharing' | 'profile_visibility';

// Consent must be explicit, informed, and specific
interface UserConsent {
  type: ConsentType;
  granted: boolean;
  timestamp: number;
  expiresAt?: number;
  informationProvided: string[];
}

// Operations requiring consent must take consent proof
interface ConsentProof {
  consentType: ConsentType;
  userId: string;
  verified: boolean;
}

// Functions requiring consent
function shareUserLocation(location: GeoLocation, consentProof: ConsentProof): void {
  if (!consentProof.verified || consentProof.consentType !== 'location_sharing') {
    throw new Error('Valid location sharing consent required');
  }
  // Implementation with guaranteed consent
}
```

### Data Provenance Types
```typescript
// Track where data came from
interface DataProvenance<T> {
  value: T;
  source: 'user_provided' | 'derived' | 'third_party';
  timestamp: number;
  processingSteps?: string[];
  consentReference?: string;
}

// Require provenance for sensitive data
function processUserData<T>(data: DataProvenance<T>): void {
  // We now know where data came from and can handle it accordingly
  if (data.source === 'third_party' && !data.consentReference) {
    throw new Error('Third-party data requires consent reference');
  }
}
```

### Privacy-Preserving API Types
```typescript
// Define what is visible to different viewers
type VisibilityLevel = 'public' | 'connections' | 'self_only';

// Tie visibility to data fields
type ProfileWithVisibility = {
  [K in keyof UserProfile]: {
    value: UserProfile[K];
    visibility: VisibilityLevel;
  }
};

// Contextual visibility that enforces privacy
function getUserProfileForViewer(
  profile: ProfileWithVisibility,
  viewerRelationship: 'self' | 'connection' | 'public'
): Partial<UserProfile> {
  const result: Partial<UserProfile> = {};
  
  for (const [key, field] of Object.entries(profile)) {
    // Enforce visibility rules through types
    if (
      field.visibility === 'public' ||
      (field.visibility === 'connections' && 
       (viewerRelationship === 'connection' || viewerRelationship === 'self')) ||
      (field.visibility === 'self_only' && viewerRelationship === 'self')
    ) {
      result[key as keyof UserProfile] = field.value;
    }
  }
  
  return result;
}
```

These TypeScript patterns ensure that ethical considerations aren't just documentation - they're enforced by the type system itself, making privacy and consent violations compile-time errors rather than runtime bugs.
""",
            "react": """
# React in ThinkAlike

ThinkAlike uses React not just as a UI library, but as a framework for implementing our ethical principles at the component level.

## Ethical React Patterns

### User Sovereignty Hooks
```tsx
// Hook for user data with built-in consent management
function useUserData<T>(
  dataType: string,
  initialValue: T
): {
  data: T;
  updateData: (value: T) => void;
  consentStatus: 'granted' | 'denied' | 'not_asked';
  requestConsent: () => Promise<boolean>;
  revokeConsent: () => void;
} {
  const [data, setData] = useState<T>(initialValue);
  const [consentStatus, setConsentStatus] = useState<'granted' | 'denied' | 'not_asked'>(
    localStorage.getItem(`consent_${dataType}`) === 'granted'
      ? 'granted'
      : localStorage.getItem(`consent_${dataType}`) === 'denied'
      ? 'denied'
      : 'not_asked'
  );
  
  // Request user consent with clear information
  const requestConsent = async () => {
    // Implementation of consent UI
    const granted = await showConsentDialog({
      dataType,
      purpose: `Store and process your ${dataType} to provide core functionality`,
      storage: 'local_with_optional_sync',
      thirdParties: 'none',
      retention: '30_days_after_account_deletion'
    });
    
    setConsentStatus(granted ? 'granted' : 'denied');
    localStorage.setItem(`consent_${dataType}`, granted ? 'granted' : 'denied');
    return granted;
  };
  
  // Users can revoke consent at any time
  const revokeConsent = () => {
    setConsentStatus('denied');
    localStorage.setItem(`consent_${dataType}`, 'denied');
    // Optionally delete data when consent revoked
  };
  
  // Only update data if consent granted
  const updateData = (value: T) => {
    if (consentStatus === 'granted') {
      setData(value);
    } else {
      console.warn(`Cannot update ${dataType} without user consent`);
    }
  };
  
  return { data, updateData, consentStatus, requestConsent, revokeConsent };
}
```

### Transparent Algorithm Components
```tsx
function AlgorithmExplainer({ algorithmId, inputData, outputResult }) {
  const [expanded, setExpanded] = useState(false);
  const [processingSteps, setProcessingSteps] = useState([]);
  
  useEffect(() => {
    // Fetch actual algorithm steps used
    if (expanded) {
      fetchAlgorithmSteps(algorithmId, inputData, outputResult)
        .then(steps => setProcessingSteps(steps));
    }
  }, [expanded, algorithmId, inputData, outputResult]);
  
  return (
    <div className="algorithm-explainer">
      <button onClick={() => setExpanded(!expanded)}>
        {expanded ? 'Hide algorithm details' : 'Why am I seeing this?'}
      </button>
      
      {expanded && (
        <div className="algorithm-steps">
          <h3>How we derived this result</h3>
          
          {processingSteps.map((step, index) => (
            <div key={index} className="algorithm-step">
              <div className="step-number">{index + 1}</div>
              <div className="step-description">{step.description}</div>
              <div className="step-data">
                Input: {JSON.stringify(step.input)}
                Output: {JSON.stringify(step.output)}
              </div>
            </div>
          ))}
          
          <div className="algorithm-principles">
            <h4>Ethical Considerations</h4>
            <ul>
              {getAlgorithmPrinciples(algorithmId).map((principle, index) => (
                <li key={index}>{principle}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
```

### User Control Patterns
```tsx
function UserControlledOperation({ 
  operationName, 
  description, 
  operation,
  autoExecute = false
}) {
  const [status, setStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
  const [userApproved, setUserApproved] = useState(autoExecute);
  const [result, setResult] = useState(null);
  
  // Auto-run if configured and user approved
  useEffect(() => {
    if (autoExecute && userApproved && status === 'idle') {
      executeOperation();
    }
  }, [userApproved, autoExecute]);
  
  const executeOperation = async () => {
    setStatus('running');
    try {
      const opResult = await operation();
      setResult(opResult);
      setStatus('completed');
    } catch (error) {
      setStatus('error');
      console.error(error);
    }
  };
  
  return (
    <div className="user-controlled-operation">
      <h3>{operationName}</h3>
      <p>{description}</p>
      
      {status === 'idle' && !userApproved && (
        <button onClick={() => setUserApproved(true)}>
          Approve and Execute
        </button>
      )}
      
      {status === 'idle' && userApproved && (
        <button onClick={executeOperation}>
          Execute Now
        </button>
      )}
      
      {status === 'running' && (
        <div className="operation-status">
          Running... <button onClick={() => setStatus('idle')}>Cancel</button>
        </div>
      )}
      
      {status === 'completed' && (
        <div className="operation-result">
          <div className="success-message">Completed Successfully</div>
          <div className="result-data">{JSON.stringify(result)}</div>
          <button onClick={() => setStatus('idle')}>Run Again</button>
        </div>
      )}
      
      {status === 'error' && (
        <div className="operation-error">
          <div className="error-message">Operation Failed</div>
          <button onClick={() => setStatus('idle')}>Try Again</button>
        </div>
      )}
    </div>
  );
}
```

These React patterns ensure that ThinkAlike's ethical principles are directly encoded into our component architecture, making them the default way of building features rather than an afterthought.
"""
        }
        
        # Fuzzy match concept to known concepts
        concept_lower = concept.lower()
        for key, content in concepts.items():
            if key in concept_lower:
                return content
                
        # Default explanation if no match
        return f"""
# {concept} in ThinkAlike

I don't have specific information about {concept} in ThinkAlike's frontend architecture yet.

Would you like to learn about one of these concepts instead?
- Components and UI Architecture
- State Management
- TypeScript Integration
- React Patterns

Or would you like to contribute documentation about {concept} to help improve ThinkAlike's resources?
"""
        
    def guided_tutorial(self, topic: str, experience_level: str = "beginner") -> List[Dict]:
        """Provide a step-by-step tutorial on a frontend topic."""
        # Tutorials would be implemented here - returning a structured format
        # This is just a placeholder
        return [
            {"type": "text", "content": f"# {topic} Tutorial for {experience_level}s"},
            {"type": "text", "content": "This would be a comprehensive tutorial with steps and code examples."},
            {"type": "code", "language": "tsx", "content": "// Example code would go here"}
        ]

def main():
    """Command-line interface for the Frontend Guardian."""
    if len(sys.argv) < 2:
        print("Please specify a command: overview, suggest, explain, or tutorial")
        sys.exit(1)
        
    command = sys.argv[1]
    guardian = FrontendGuardian()
    
    if command == "overview":
        print(guardian.get_project_overview())
    elif command == "suggest":
        experience = sys.argv[2] if len(sys.argv) > 2 else "beginner"
        print(guardian.suggest_first_contribution(experience))
    elif command == "explain":
        if len(sys.argv) < 3:
            print("Please specify a concept to explain")
            sys.exit(1)
        concept = sys.argv[2]
        print(guardian.explain_frontend_concept(concept))
    elif command == "tutorial":
        if len(sys.argv) < 3:
            print("Please specify a tutorial topic")
            sys.exit(1)
        topic = sys.argv[2]
        experience = sys.argv[3] if len(sys.argv) > 3 else "beginner"
        tutorial = guardian.guided_tutorial(topic, experience)
        for step in tutorial:
            if step["type"] == "text":
                print(step["content"])
            elif step["type"] == "code":
                print(f"```{step['language']}\n{step['content']}\n```")
    else:
        print(f"Unknown command: {command}")
        print("Available commands: overview, suggest, explain, tutorial")
        sys.exit(1)

if __name__ == "__main__":
    main()