import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SecurityStatusIndicator } from './SecurityStatusIndicator';
import { securityStore } from '../../stores/securityStore';

// Mock the security store
jest.mock('../../stores/securityStore', () => ({
  securityStore: {
    status: 'secure',
    protocols: [
      { name: 'HTTPS', active: true, timestamp: '2025-04-12T09:18:08.291Z' },
      { name: 'JWT', active: true, timestamp: '2025-04-12T09:18:08.294Z' },
      { name: 'Data Encryption', active: true, timestamp: '2025-04-12T09:18:08.299Z' }
    ],
    transparencyLevel: 'full',
    setStatus: jest.fn(),
    addProtocol: jest.fn(),
    triggerBreachAlert: jest.fn()
  }
}));

describe('SecurityStatusIndicator', () => {
  beforeEach(() => {
    // Reset mocks between tests
    jest.clearAllMocks();
  });

  test('renders secure state with green indicator', () => {
    render(<SecurityStatusIndicator />);
    const indicator = screen.getByTestId('security-status-icon');
    expect(indicator).toHaveClass('status-secure');
    expect(indicator).toHaveAttribute('title', 'Security Status: Secure');
  });

  test('shows protocol log on hover', async () => {
    render(<SecurityStatusIndicator />);
    const indicator = screen.getByTestId('security-status-icon');

    // Hover over the indicator
    fireEvent.mouseEnter(indicator);

    // Wait for the tooltip to appear
    const protocolLog = await screen.findByTestId('protocol-log');
    expect(protocolLog).toBeVisible();
    expect(protocolLog).toHaveTextContent('HTTPS');
    expect(protocolLog).toHaveTextContent('JWT');
  });

  test('changes to warning state when status changes', async () => {
    // Initial render with secure status
    const { rerender } = render(<SecurityStatusIndicator />);

    // Update the mock store to warning state
    const warningStore = {
      ...securityStore,
      status: 'warning',
      warnings: [{ type: 'partial_encryption', message: 'Some data is not encrypted' }]
    };

    // Re-render with new state
    rerender(<SecurityStatusIndicator securityStore={warningStore} />);

    // Check that the indicator changed
    const indicator = screen.getByTestId('security-status-icon');
    expect(indicator).toHaveClass('status-warning');
    expect(indicator).toHaveAttribute('title', 'Security Status: Warning');
  });

  test('triggers breach alert notification', async () => {
    // Set up breach alert in store
    const breachStore = {
      ...securityStore,
      status: 'breach',
      breachDetails: {
        type: 'unauthorized_access',
        timestamp: '2025-04-12T10:25:16.128Z',
        severity: 'critical',
        message: 'Unauthorized access detected'
      }
    };

    render(<SecurityStatusIndicator securityStore={breachStore} />);

    // Check that indicator shows breach state
    const indicator = screen.getByTestId('security-status-icon');
    expect(indicator).toHaveClass('status-breach');

    // Check that a notification is displayed
    const alert = await screen.findByRole('alert');
    expect(alert).toBeVisible();
    expect(alert).toHaveTextContent('Unauthorized access detected');
  });
});
