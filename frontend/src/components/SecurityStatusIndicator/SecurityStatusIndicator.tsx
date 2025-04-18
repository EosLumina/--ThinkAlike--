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
const StatusIcon: React.FC<{ level: string }> = ({ level }: { level: string }) => {
  return <span className={`icon status-icon-${level?.toLowerCase()}`}>🔒</span>;
};

const ProtocolLogPopover: React.FC<{ logData: Array<{ timestamp: string; message: string }>; children: React.ReactNode }> = ({ logData, children }: { logData: Array<{ timestamp: string; message: string }>; children: React.ReactNode }) => {
  const [isVisible, setIsVisible] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);
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
              {logData.map((entry: { timestamp: string; message: string }, index: number) => (
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

const AlertIcon: React.FC<{ severity: string }> = ({ severity }: { severity: string }) => {
  return <span className={`icon alert-icon severity-${severity?.toLowerCase()}`}>⚠️</span>;
};

const SettingsLink: React.FC = () => {
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
