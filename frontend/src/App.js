import CircularProgress from '@mui/material/CircularProgress';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes, useParams } from 'react-router-dom';

// Components
import DataTraceability from './components/DataTraceability';
import Navigation from './components/Navigation';
import EventProximity from './components/location/EventProximity';
import LocationSharing from './components/location/LocationSharing';

// Contexts
import { AuthProvider } from './contexts/AuthContext';
import { DataTraceabilityProvider } from './contexts/DataTraceabilityContext';

import './App.css';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
    }
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [dataFlow, setDataFlow] = useState({ nodes: [], edges: [] }); // Initialize with empty data
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/api/v1/graph') // Fetch from the backend API
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setDataFlow(data); // Update state with fetched data
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []); // Empty dependency array: run once on mount

  const toggleConnectionStatus = () => {
    setConnectionStatus(prevStatus => {
      if (prevStatus === 'disconnected') {
        return 'connecting';
      } else if (prevStatus === 'connecting') {
        return 'connected';
      } else {
        return 'disconnected';
      }
    });
  };

  return (
    <AuthProvider>
      <DataTraceabilityProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router>
            <div className="App">
              <Navigation />

              <section className="content">
                {loading ? (
                  <div className="loading-container">
                    <CircularProgress />
                    <Typography variant="body1" sx={{ mt: 2 }}>
                      Loading...
                    </Typography>
                  </div>
                ) : error ? (
                  <div className="error-container">
                    <Typography variant="h6" color="error">
                      Error: {error}
                    </Typography>
                  </div>
                ) : (
                  <Routes>
                    <Route path="/" element={<DataTraceability dataFlow={dataFlow} connectionStatus={connectionStatus} />} />
                    <Route path="/location-sharing" element={<LocationSharing />} />
                    <Route path="/events/:eventId/proximity" element={<EventProximityWrapper />} />
                    <Route path="*" element={<Navigate to="/" />} />
                  </Routes>
                )}
              </section>
            </div>
          </Router>
        </ThemeProvider>
      </DataTraceabilityProvider>
    </AuthProvider>
  );
}

const EventProximityWrapper = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await axios.get(`/api/v1/events/${eventId}`);
        setEvent(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [eventId]);

  if (loading) return <CircularProgress />;
  if (!event) return <Typography>Event not found</Typography>;

  return <EventProximity eventId={eventId} eventName={event.event_name} />;
};

export default App;
