import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';
import { useDataTraceability } from '../../contexts/DataTraceabilityContext';
import { 
  Box, Button, Typography, CircularProgress, Alert, Paper, Chip,
  List, ListItem, ListItemText, ListItemIcon, Switch, FormControlLabel,
  Divider, Avatar, Grid
} from '@mui/material';
import { 
  PersonPin, Event, NotListedLocation, CheckCircle, 
  ErrorOutline, AccessTime, PeopleAlt
} from '@mui/icons-material';

/**
 * EventProximity component for ThinkAlike
 * Shows nearby attendees at events with user consent and privacy preservation
 */
const EventProximity = ({ eventId, eventName }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [optedIn, setOptedIn] = useState(false);
  const [nearbyAttendees, setNearbyAttendees] = useState([]);
  const [expiresAt, setExpiresAt] = useState(null);
  const { token } = useAuth();
  const { trackDataUsage } = useDataTraceability();

  // Check if user is opted in when component mounts
  useEffect(() => {
    checkOptInStatus();
  }, [eventId]);
  
  // Fetch nearby attendees when opted in status changes
  useEffect(() => {
    if (optedIn) {
      fetchNearbyAttendees();
    }
  }, [optedIn]);

  const checkOptInStatus = async () => {
    try {
      // This would be an actual API call in production
      // Here we just simulate with mock data
      setLoading(true);
      
      // Try to fetch nearby attendees - if it succeeds, user is opted in
      try {
        const response = await axios.get(`/api/v1/events/${eventId}/nearby_attendees`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setOptedIn(true);
        setNearbyAttendees(response.data.attendees);
        
        // Log for data traceability
        trackDataUsage({
          action: 'check_proximity_opt_in',
          dataType: 'proximity_status',
          purpose: 'Check if user has opted into proximity sharing',
          accessType: 'read',
          userConsent: true
        });
      } catch (err) {
        // If we get a 403, user is not opted in
        if (err.response && err.response.status === 403) {
          setOptedIn(false);
        } else {
          throw err; // Re-throw for the outer catch
        }
      }
    } catch (err) {
      console.error(err);
      setError('Failed to check opt-in status');
    } finally {
      setLoading(false);
    }
  };

  const handleOptIn = async () => {
    try {
      setLoading(true);
      
      // Log for data traceability
      trackDataUsage({
        action: 'opt_in_to_proximity',
        dataType: 'location',
        purpose: 'Enable proximity awareness for event',
        accessType: 'create',
        eventId,
        userConsent: true
      });
      
      const response = await axios.post(`/api/v1/events/${eventId}/proximity_opt_in`, {
        duration: 120 // Default to 2 hours
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setOptedIn(true);
      setExpiresAt(response.data.expiresAt);
      fetchNearbyAttendees();
    } catch (err) {
      console.error(err);
      setError('Failed to opt in to proximity sharing');
    } finally {
      setLoading(false);
    }
  };

  const handleOptOut = async () => {
    try {
      setLoading(true);
      
      // Log for data traceability
      trackDataUsage({
        action: 'opt_out_from_proximity',
        dataType: 'location',
        purpose: 'Disable proximity awareness for event',
        accessType: 'delete',
        eventId,
        userConsent: true
      });
      
      // In a real implementation, this would be an actual API call
      // Here we just simulate success
      setTimeout(() => {
        setOptedIn(false);
        setNearbyAttendees([]);
      }, 1000);
      
    } catch (err) {
      console.error(err);
      setError('Failed to opt out from proximity sharing');
    } finally {
      setLoading(false);
    }
  };

  const fetchNearbyAttendees = async () => {
    if (!optedIn) return;
    
    try {
      setLoading(true);
      
      // Log for data traceability
      trackDataUsage({
        action: 'fetch_nearby_attendees',
        dataType: 'anonymized_proximity',
        purpose: 'View nearby event attendees',
        accessType: 'read',
        eventId,
        userConsent: true
      });
      
      const response = await axios.get(`/api/v1/events/${eventId}/nearby_attendees`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setNearbyAttendees(response.data.attendees);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch nearby attendees');
    } finally {
      setLoading(false);
    }
  };

  // Helper to determine avatar color based on proximity
  const getProximityColor = (proximity) => {
    switch (proximity) {
      case 'Nearby':
        return '#4CAF50'; // Green
      case 'Within 200m':
        return '#2196F3'; // Blue
      case 'Within venue':
      case 'Within 500m':
        return '#FFC107'; // Amber
      default:
        return '#9E9E9E'; // Grey
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4, maxWidth: 800, margin: '0 auto' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Event sx={{ mr: 1 }} />
        <Typography variant="h5" component="h2">
          {eventName || 'Event Proximity'}
        </Typography>
      </Box>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>Privacy Notice:</strong> Location data is anonymized and only shared with other opted-in attendees.
          Only approximate distances are shown. You can opt out at any time.
        </Typography>
      </Alert>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      {/* Opt-in toggle */}
      <Paper variant="outlined" sx={{ p: 2, mb: 3, backgroundColor: optedIn ? '#f0f7ff' : '#f5f5f5' }}>
        <FormControlLabel
          control={
            <Switch 
              checked={optedIn} 
              onChange={optedIn ? handleOptOut : handleOptIn}
              disabled={loading}
            />
          }
          label={
            <Box>
              <Typography variant="subtitle1" sx={{ fontWeight: 'medium' }}>
                {optedIn ? 'Proximity Sharing Enabled' : 'Enable Proximity Sharing'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {optedIn 
                  ? 'Other attendees can see your approximate location at this event' 
                  : 'Allow others to see your approximate location at this event'}
              </Typography>
              {expiresAt && optedIn && (
                <Typography variant="caption" sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                  <AccessTime sx={{ fontSize: '0.9rem', mr: 0.5 }} />
                  Expires: {new Date(expiresAt).toLocaleString()}
                </Typography>
              )}
            </Box>
          }
          sx={{ width: '100%', m: 0 }}
        />
      </Paper>
      
      {/* Nearby attendees list */}
      {optedIn && (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
              <PeopleAlt sx={{ mr: 1, fontSize: '1.2rem' }} /> 
              Nearby Attendees
            </Typography>
            <Button 
              size="small" 
              onClick={fetchNearbyAttendees}
              disabled={loading}
            >
              Refresh
            </Button>
          </Box>
          
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
              <CircularProgress size={30} />
            </Box>
          ) : nearbyAttendees.length > 0 ? (
            <Grid container spacing={2}>
              {nearbyAttendees.map((attendee) => (
                <Grid item xs={12} sm={6} md={4} key={attendee.userId}>
                  <Paper 
                    variant="outlined" 
                    sx={{ 
                      p: 2,
                      display: 'flex',
                      alignItems: 'center',
                      borderLeft: `4px solid ${getProximityColor(attendee.proximityCategory)}`
                    }}
                  >
                    <Avatar 
                      sx={{ 
                        bgcolor: getProximityColor(attendee.proximityCategory),
                        mr: 1.5
                      }}
                    >
                      <PersonPin />
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2">
                        {attendee.displayName}
                      </Typography>
                      <Chip 
                        label={attendee.proximityCategory} 
                        size="small" 
                        sx={{ mt: 0.5, fontWeight: 'medium' }}
                      />
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Box sx={{ textAlign: 'center', py: 3 }}>
              <NotListedLocation sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
              <Typography variant="body1">
                No nearby attendees found
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Either no one else has opted in, or no one is nearby at the moment
              </Typography>
            </Box>
          )}
        </>
      )}
    </Paper>
  );
};

export default EventProximity;