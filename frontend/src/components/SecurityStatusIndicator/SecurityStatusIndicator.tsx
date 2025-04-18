// filepath: /workspaces/--ThinkAlike--/frontend/src/components/SecurityStatusIndicator/SecurityStatusIndicator.tsx
import React, { useRef, useState } from 'react';
import { useSecurityStore } from '../../stores/securityStore';

// Placeholder components with basic structure and prop types
const StatusIcon = ({ level }: { level: string }) => {
  return <span className={`icon status-icon-${level?.toLowerCase()}`}>🔒</span>;
};

const ProtocolLogPopover = ({ logData, children }: { logData: Array<{ timestamp: string; message: string }>; children: React.ReactNode }) => {
  const [isVisible, setIsVisible] = useState(false);
  const popoverRef = useRef<HTMLDivElement | null>(null);
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

const AlertIcon = ({ severity }: { severity: string }) => {
  return <span className={`icon alert-icon severity-${severity?.toLowerCase()}`}>⚠️</span>;
};

const SettingsLink = () => {
  return <a href="/security-center" aria-label="Security Settings" className="settings-link">⚙️</a>;
};

// Main Component
export const SecurityStatusIndicator: React.FunctionComponent = () => {
  const { securityStatus, breachAlert } = useSecurityStore();
  const currentLevel = securityStatus?.level || 'Amber';
  const currentLogs = securityStatus?.logs || [];
  return (
    <div className={`security-indicator status-${currentLevel.toLowerCase()}`}>
      <ProtocolLogPopover logData={currentLogs}>
        <StatusIcon level={currentLevel} />
        {breachAlert && <AlertIcon severity={breachAlert.severity} />}
      </ProtocolLogPopover>
      <SettingsLink />
    </div>
  );
};
