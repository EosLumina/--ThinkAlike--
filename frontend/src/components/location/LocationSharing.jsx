import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';
import { useDataTraceability } from '../../contexts/DataTraceabilityContext';
import { Box, Button, Typography, CircularProgress, Alert, 
         Dialog, DialogActions, DialogContent, DialogContentText, 
         DialogTitle, Select, MenuItem, TextField, FormControl,
         InputLabel, Chip } from '@mui/material';
import { LocationOn, Close, AccessTime, Share, People } from '@mui/icons-material';

/**
 * LocationSharing component for ThinkAlike
 * Handles initiating, managing and stopping location sharing
 * Implements ethical data handling with user consent and transparency
 */
const LocationSharing = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeShares, setActiveShares] = useState({ initiated: [], received: [] });
  const [openShareDialog, setOpenShareDialog] = useState(false);
  const [recipientId, setRecipientId] = useState('');
  const [duration, setDuration] = useState(30); // 30 minutes default
  const [message, setMessage] = useState('');
  const [availableRecipients, setAvailableRecipients] = useState([]);
  const { token, user } = useAuth();
  const { trackDataUsage } = useDataTraceability();

  // Fetch active shares when component mounts
  useEffect(() => {
    fetchActiveShares();
    fetchAvailableRecipients();
  }, []);

  const fetchActiveShares = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/v1/location/active_shares', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setActiveShares(response.data);
      
      // Log for data traceability
      trackDataUsage({
        action: 'fetch_location_shares',
        dataType: 'location_metadata',
        purpose: 'Display active location shares',
        accessType: 'read',
        userConsent: true
      });
    } catch (err) {
      setError('Failed to load active location shares');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableRecipients = async () => {
    // In a real app, this would fetch the user's connections
    // Here we just simulate with mock data
    setAvailableRecipients([
      { id: 'user-123', name: 'Alice Johnson' },
      { id: 'user-456', name: 'Bob Smith' },
      { id: 'group-789', name: 'Hiking Club' }
    ]);
  };

  const handleShareLocation = async () => {
    if (!recipientId) {
      setError('Please select a recipient');
      return;
    }

    try {
      setLoading(true);
      
      // Log for data traceability before sharing
      trackDataUsage({
        action: 'initiate_location_share',
        dataType: 'live_location',
        purpose: 'Share location with selected recipient',
        accessType: 'share',
        recipientId,
        duration,
        userConsent: true
      });
      
      const response = await axios.post('/api/v1/location/share_live', {
        recipientId,
        durationMinutes: duration,
        message
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      await fetchActiveShares();
      setOpenShareDialog(false);
      setRecipientId('');
      setMessage('');
    } catch (err) {
      setError('Failed to share location. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStopSharing = async (shareId) => {
    try {
      setLoading(true);
      
      // Log for data traceability
      trackDataUsage({
        action: 'stop_location_share',
        dataType: 'live_location',
        purpose: 'Stop sharing location',
        accessType: 'delete',
        shareId,
        userConsent: true
      });
      
      await axios.post('/api/v1/location/stop_sharing', {
        shareId
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      await fetchActiveShares();
    } catch (err) {
      setError('Failed to stop location sharing');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Duration options in minutes
  const durationOptions = [15, 30, 60, 120, 240, 480];

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', padding: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <LocationOn sx={{ mr: 1 }} /> Location Sharing
      </Typography>
      
      {/* Privacy notice/consent reminder */}
      <Alert severity="info" sx={{ mb: 3 }}>
        Location data is only shared with the people you explicitly choose, for the duration you specify. 
        You can stop sharing anytime. Your data is encrypted end-to-end.
      </Alert>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      {/* Action buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<Share />}
          onClick={() => setOpenShareDialog(true)}
        >
          Share My Location
        </Button>
        
        <Button 
          variant="outlined"
          onClick={fetchActiveShares}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>
      
      {/* Active shares sections */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* Shares initiated by user */}
          <Typography variant="h6" gutterBottom>You are sharing with:</Typography>
          {activeShares.initiated && activeShares.initiated.length > 0 ? (
            activeShares.initiated.map((share) => (
              <Box 
                key={share.shareId}
                sx={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  p: 2, 
                  mb: 2, 
                  border: '1px solid #ddd', 
                  borderRadius: 1,
                  backgroundColor: '#f5f5f5'
                }}
              >
                <Box>
                  <Typography variant="subtitle1">
                    <strong>{share.recipientName}</strong>
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center' }}>
                    <AccessTime sx={{ fontSize: '0.9rem', mr: 0.5 }} />
                    Expires: {new Date(share.expiresAt).toLocaleString()}
                  </Typography>
                </Box>
                <Button 
                  variant="outlined" 
                  color="error" 
                  startIcon={<Close />}
                  onClick={() => handleStopSharing(share.shareId)}
                >
                  Stop Sharing
                </Button>
              </Box>
            ))
          ) : (
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              You are not currently sharing your location with anyone.
            </Typography>
          )}
          
          {/* Shares received by user */}
          <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>Sharing with you:</Typography>
          {activeShares.received && activeShares.received.length > 0 ? (
            activeShares.received.map((share) => (
              <Box 
                key={share.shareId}
                sx={{ 
                  p: 2, 
                  mb: 2, 
                  border: '1px solid #ddd', 
                  borderRadius: 1,
                  backgroundColor: '#eef7ff'
                }}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="subtitle1">
                    <strong>{share.senderName}</strong> is sharing their location
                  </Typography>
                  <Chip 
                    label="Active" 
                    color="success" 
                    size="small" 
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1, display: 'flex', alignItems: 'center' }}>
                  <AccessTime sx={{ fontSize: '0.9rem', mr: 0.5 }} />
                  Until: {new Date(share.expiresAt).toLocaleString()}
                </Typography>
                <Button 
                  variant="text" 
                  color="primary"
                  sx={{ mt: 1 }}
                >
                  View on map
                </Button>
              </Box>
            ))
          ) : (
            <Typography variant="body1" color="text.secondary">
              No one is currently sharing their location with you.
            </Typography>
          )}
        </>
      )}
      
      {/* Share location dialog */}
      <Dialog open={openShareDialog} onClose={() => setOpenShareDialog(false)}>
        <DialogTitle>Share Your Location</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ mb: 2 }}>
            Choose who you want to share your location with and for how long.
            They will be able to see your real-time location during this period.
          </DialogContentText>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel id="recipient-label">Share with</InputLabel>
            <Select
              labelId="recipient-label"
              value={recipientId}
              onChange={(e) => setRecipientId(e.target.value)}
              label="Share with"
            >
              {availableRecipients.map((recipient) => (
                <MenuItem key={recipient.id} value={recipient.id}>
                  {recipient.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel id="duration-label">Duration</InputLabel>
            <Select
              labelId="duration-label"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              label="Duration"
            >
              {durationOptions.map((mins) => (
                <MenuItem key={mins} value={mins}>
                  {mins < 60 ? `${mins} minutes` : `${mins/60} hour${mins > 60 ? 's' : ''}`}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <TextField
            fullWidth
            label="Message (optional)"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenShareDialog(false)}>Cancel</Button>
          <Button 
            onClick={handleShareLocation} 
            variant="contained" 
            color="primary"
            disabled={loading || !recipientId}
          >
            {loading ? <CircularProgress size={24} /> : 'Share Location'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default LocationSharing;