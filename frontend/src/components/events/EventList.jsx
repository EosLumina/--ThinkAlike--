import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, CardActions, Button, Chip, 
         Grid, CircularProgress, TextField, InputAdornment } from '@mui/material';
import { Search, Event, LocationOn, AccessTime, People } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useDataTraceability } from '../../contexts/DataTraceabilityContext';
import axios from 'axios';

const EventList = ({ communityId = null }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const { token } = useAuth();
  const { trackDataUsage } = useDataTraceability();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        const params = { upcoming_only: true };
        if (communityId) params.community_id = communityId;
        
        // Track data usage for transparency
        trackDataUsage({
          action: 'view_events_list',
          dataType: 'event_data',
          purpose: 'Display upcoming community events',
          accessType: 'read',
          userConsent: true
        });
        
        const response = await axios.get('/api/v1/events', { 
          params,
          headers: { Authorization: `Bearer ${token}` }
        });
        
        setEvents(response.data.events || []);
      } catch (error) {
        console.error('Error fetching events:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchEvents();
  }, [communityId, token, trackDataUsage]);

  // Filter events based on search term
  const filteredEvents = events.filter(event => 
    event.event_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.location?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleViewEvent = (eventId) => {
    navigate(`/events/${eventId}`);
  };

  const handleProximityView = (eventId) => {
    navigate(`/events/${eventId}/proximity`);
  };

  // Format date for display
  const formatEventDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, { 
      weekday: 'short',
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Box sx={{ width: '100%', p: 2 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <Event sx={{ mr: 1 }} />
        {communityId ? 'Community Events' : 'Upcoming Events'}
      </Typography>
      
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search events..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
      />
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : filteredEvents.length === 0 ? (
        <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', my: 4 }}>
          No upcoming events found.
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {filteredEvents.map(event => (
            <Grid item xs={12} sm={6} md={4} key={event.event_id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" gutterBottom>
                    {event.event_name}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <AccessTime fontSize="small" color="action" sx={{ mr: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      {formatEventDate(event.start_time)}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <LocationOn fontSize="small" color="action" sx={{ mr: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      {event.location || 'No location specified'}
                    </Typography>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {event.description?.substring(0, 120)}
                    {event.description?.length > 120 ? '...' : ''}
                  </Typography>
                  
                  {event.geofence_parameters && (
                    <Chip 
                      icon={<People size="small" />}
                      label="Proximity Enabled" 
                      size="small" 
                      color="primary" 
                      variant="outlined"
                      sx={{ mb: 1 }}
                    />
                  )}
                </CardContent>
                
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button 
                    size="small" 
                    onClick={() => handleViewEvent(event.event_id)}
                  >
                    Details
                  </Button>
                  
                  {event.geofence_parameters && (
                    <Button 
                      size="small"
                      color="primary"
                      onClick={() => handleProximityView(event.event_id)}
                    >
                      View Proximity
                    </Button>
                  )}
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default EventList;