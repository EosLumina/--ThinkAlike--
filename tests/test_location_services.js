import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import LocationSharing from '../frontend/src/components/location/LocationSharing';
import EventProximity from '../frontend/src/components/location/EventProximity';
import { AuthProvider } from '../frontend/src/contexts/AuthContext';
import { DataTraceabilityProvider } from '../frontend/src/contexts/DataTraceabilityContext';

// Mock axios
jest.mock('axios');

// Mock authentication context
jest.mock('../frontend/src/contexts/AuthContext', () => ({
  useAuth: () => ({
    token: 'fake-token',
    user: { user_id: 'user-123', username: 'testuser' },
    isAuthenticated: true
  }),
  AuthProvider: ({ children }) => children
}));

// Mock data traceability context
jest.mock('../frontend/src/contexts/DataTraceabilityContext', () => ({
  useDataTraceability: () => ({
    trackDataUsage: jest.fn(),
    dataUsageLog: []
  }),
  DataTraceabilityProvider: ({ children }) => children
}));

describe('LocationSharing Component', () => {
  beforeEach(() => {
    axios.get.mockReset();
    axios.post.mockReset();
  });

  test('renders location sharing component', async () => {
    axios.get.mockResolvedValueOnce({ data: { initiated: [], received: [] } });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <LocationSharing />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    expect(await screen.findByText(/Location Sharing/i)).toBeInTheDocument();
    expect(screen.getByText(/You are not currently sharing your location with anyone/i)).toBeInTheDocument();
  });

  test('shows active shares when available', async () => {
    const mockData = {
      initiated: [
        {
          shareId: 'share-123',
          recipientId: 'user-456',
          recipientName: 'Jane Doe',
          expiresAt: '2023-04-05T12:00:00Z'
        }
      ],
      received: []
    };
    
    axios.get.mockResolvedValueOnce({ data: mockData });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <LocationSharing />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    expect(await screen.findByText(/Jane Doe/i)).toBeInTheDocument();
    expect(screen.getByText(/Stop Sharing/i)).toBeInTheDocument();
  });

  test('handles share location dialog', async () => {
    axios.get.mockResolvedValueOnce({ data: { initiated: [], received: [] } });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <LocationSharing />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    // Open dialog
    const shareButton = await screen.findByText(/Share My Location/i);
    fireEvent.click(shareButton);
    
    // Dialog should be visible
    expect(screen.getByText(/Choose who you want to share your location with/i)).toBeInTheDocument();
    
    // Close dialog
    const cancelButton = screen.getByText(/Cancel/i);
    fireEvent.click(cancelButton);
    
    // Dialog should be closed
    expect(screen.queryByText(/Choose who you want to share your location with/i)).not.toBeInTheDocument();
  });
});

describe('EventProximity Component', () => {
  beforeEach(() => {
    axios.get.mockReset();
    axios.post.mockReset();
  });
  
  test('renders event proximity component with opt-in toggle', async () => {
    axios.get.mockRejectedValueOnce({ response: { status: 403 } });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <EventProximity eventId="event-123" eventName="Testing Event" />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    expect(await screen.findByText(/Testing Event/i)).toBeInTheDocument();
    expect(screen.getByText(/Enable Proximity Sharing/i)).toBeInTheDocument();
  });
  
  test('shows nearby attendees when opted in', async () => {
    axios.get.mockResolvedValueOnce({ 
      data: { 
        attendees: [
          {
            userId: 'user-789',
            displayName: 'John Smith',
            proximityCategory: 'Nearby',
            lastUpdated: '2023-04-05T12:00:00Z'
          }
        ]
      }
    });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <EventProximity eventId="event-123" eventName="Testing Event" />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    expect(await screen.findByText(/John Smith/i)).toBeInTheDocument();
    expect(screen.getByText(/Nearby/i)).toBeInTheDocument();
  });
  
  test('handles opt-in to proximity sharing', async () => {
    axios.get.mockRejectedValueOnce({ response: { status: 403 } });
    axios.post.mockResolvedValueOnce({ 
      data: { 
        message: 'Successfully opted into proximity sharing',
        eventId: 'event-123',
        eventName: 'Testing Event',
        expiresAt: '2023-04-05T14:00:00Z'
      }
    });
    axios.get.mockResolvedValueOnce({ data: { attendees: [] } });
    
    render(
      <AuthProvider>
        <DataTraceabilityProvider>
          <EventProximity eventId="event-123" eventName="Testing Event" />
        </DataTraceabilityProvider>
      </AuthProvider>
    );
    
    // Wait for component to load
    await screen.findByText(/Enable Proximity Sharing/i);
    
    // Toggle opt-in
    const toggle = screen.getByRole('checkbox');
    fireEvent.click(toggle);
    
    // Should show nearby attendees section
    expect(await screen.findByText(/Nearby Attendees/i)).toBeInTheDocument();
  });
});