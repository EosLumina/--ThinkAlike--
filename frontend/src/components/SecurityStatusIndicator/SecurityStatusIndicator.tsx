// filepath: /workspaces/--ThinkAlike--/frontend/src/components/SecurityStatusIndicator/SecurityStatusIndicator.tsx
import React, { useRef, useState } from 'react'; // Added useContext
import { useSecurityStore } from '../../stores/securityStore';

// Define interfaces for props
interface StatusIconProps {
  level: 'Blue' | 'Amber' | 'NeonOrange' | string; // Use specific levels if known, else string
}

interface ProtocolLogPopoverProps {
  logData: Array<{ timestamp: string; message: string }>; // Assuming log structure
  children: React.ReactNode;
}

interface AlertIconProps {
  severity: 'high' | 'medium' | 'low' | string; // Use specific severities if known, else string
}

// Define the shape of the security context/store data
// This should match the structure provided by useSecurityStore
// and the types defined in securityStore.d.ts
interface SecurityContextValue {
  securityStatus: {
    level: string;
    logs: Array<{ timestamp: string; message: string }>;
  };
  breachAlert: {
    severity: string;
  } | null;
}

// Placeholder components with basic structure and prop types
const StatusIcon: React.FC<StatusIconProps> = ({ level }) => {
  // Basic implementation - replace with actual icon logic
  return <span className={`icon status-icon-${level?.toLowerCase()}`}>🔒</span>; // Added nullish coalescing for safety
};

const ProtocolLogPopover: React.FC<ProtocolLogPopoverProps> = ({ logData, children }) => {
  const [isVisible, setIsVisible] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);

  // Basic popover logic - replace with actual implementation (e.g., using a library)
  return (
    <div
      className="popover-container"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div ref={popoverRef} className="popover-content security-log-popover">
          <h4>Security Log</h4>
          {logData && logData.length > 0 ? (
            <ul>
              {logData.map((entry, index) => (
                <li key={index}>[{entry.timestamp}] {entry.message}</li>
              ))}
            </ul>
          ) : (
            <p>No recent security events.</p>
          )}
        </div>
      )}
    </div>
  );
};

const AlertIcon: React.FC<AlertIconProps> = ({ severity }) => {
  // Basic implementation - replace with actual icon logic
  return <span className={`icon alert-icon severity-${severity?.toLowerCase()}`}>⚠️</span>; // Added nullish coalescing for safety
};

const SettingsLink: React.FC = () => {
  // Basic implementation - replace with actual link/button logic
  return <a href="/security-center" aria-label="Security Settings" className="settings-link">⚙️</a>;
};

// Main Component
export const SecurityStatusIndicator: React.FC = () => {
  // Use the hook and assert the type based on the interface
  const { securityStatus, breachAlert } = useSecurityStore() as SecurityContextValue;

  // Default values or loading state handling might be needed
  const currentLevel = securityStatus?.level || 'Amber'; // Default to Amber if status is unavailable
  const currentLogs = securityStatus?.logs || [];

  return (
    <div className={`security-indicator status-${currentLevel.toLowerCase()}`}>
      <ProtocolLogPopover logData={currentLogs}>
        {/* Ensure StatusIcon receives a valid level string */}
        <StatusIcon level={currentLevel} />
        {breachAlert && <AlertIcon severity={breachAlert.severity} />}
      </ProtocolLogPopover>
      <SettingsLink />
    </div>
  );
};
