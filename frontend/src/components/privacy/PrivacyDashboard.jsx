import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useDataTraceability } from '../../contexts/DataTraceabilityContext';
import {
  Box, Typography, Paper, Switch, FormControl, FormControlLabel,
  Divider, Accordion, AccordionSummary, AccordionDetails,
  Alert, Button, CircularProgress, Grid, Chip, Tooltip
} from '@mui/material';
import {
  ExpandMore, Security, Visibility, VisibilityOff,
  LocationOn, Person, Group, DataUsage, Delete
} from '@mui/icons-material';
import axios from 'axios';

const PrivacyDashboard = () => {
  const { token, user } = useAuth();
  const { trackDataUsage } = useDataTraceability();
  const [loading, setLoading] = useState(true);
  const [privacySettings, setPrivacySettings] = useState({
    locationSharing: false,
    profileVisibility: 'friends', // 'public', 'friends', 'private'
    dataRetention: 30, // days
    communityDiscoverability: true,
    thirdPartySharing: false,
    dataAnalyticsConsent: true
  });
  const [dataUsageHistory, setDataUsageHistory] = useState([]);
  
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await axios.get('/api/v1/users/privacy-settings', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setPrivacySettings(response.data);
        
        // Log this access for transparency
        trackDataUsage({
          action: 'view_privacy_settings',
          dataType: 'privacy_preferences',
          purpose: 'Display current privacy configuration',
          accessType: 'read',
          userConsent: true
        });
        
        // Also fetch data usage history
        const historyResponse = await axios.get('/api/v1/data-traceability/history', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setDataUsageHistory(historyResponse.data.slice(0, 10)); // Last 10 events
      } catch (err) {
        console.error("Error fetching privacy settings:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchSettings();
  }, [token]);

  const handleSettingChange = async (setting, value) => {
    try {
      setLoading(true);
      
      // Track this change for transparency
      trackDataUsage({
        action: 'update_privacy_setting',
        dataType: 'privacy_preference',
        setting,
        newValue: value,
        purpose: 'Update user privacy preferences',
        accessType: 'write',
        userConsent: true
      });
      
      await axios.patch(
        '/api/v1/users/privacy-settings',
        { [setting]: value },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setPrivacySettings(prev => ({
        ...prev,
        [setting]: value
      }));
      
    } catch (err) {
      console.error("Error updating privacy setting:", err);
    } finally {
      setLoading(false);
    }
  };
  
  const requestDataDeletion = async () => {
    if (window.confirm("Are you sure you want to request deletion of all your data? This action cannot be undone.")) {
      try {
        await axios.post(
          '/api/v1/users/request-data-deletion',
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert("Data deletion request submitted. You'll receive an email confirmation shortly.");
      } catch (err) {
        console.error("Error requesting data deletion:", err);
        alert("There was an error processing your request. Please try again.");
      }
    }
  };

  if (loading && !privacySettings) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <Security sx={{ mr: 1 }} /> Privacy Dashboard
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        Your privacy is our priority. Control exactly what data is shared and with whom.
        All changes take effect immediately.
      </Alert>
      
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>Privacy Settings</Typography>
        
        <FormControlLabel
          control={
            <Switch
              checked={privacySettings.locationSharing}
              onChange={(e) => handleSettingChange('locationSharing', e.target.checked)}
              color="primary"
            />
          }
          label={
            <Box>
              <Typography variant="subtitle1">Location Sharing</Typography>
              <Typography variant="body2" color="text.secondary">
                Allow others to see your location when explicitly shared
              </Typography>
            </Box>
          }
          sx={{ display: 'flex', mb: 2 }}
        />
        
        <FormControl fullWidth sx={{ mb: 2 }}>
          <Typography variant="subtitle1">Profile Visibility</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Control who can view your profile information
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Paper 
                elevation={privacySettings.profileVisibility === 'public' ? 3 : 1}
                sx={{ 
                  p: 2, 
                  textAlign: 'center',
                  cursor: 'pointer',
                  bgcolor: privacySettings.profileVisibility === 'public' ? 'rgba(25, 118, 210, 0.1)' : 'transparent',
                  borderColor: privacySettings.profileVisibility === 'public' ? 'primary.main' : 'transparent',
                  borderWidth: 1,
                  borderStyle: 'solid'
                }}
                onClick={() => handleSettingChange('profileVisibility', 'public')}
              >
                <Visibility color={privacySettings.profileVisibility === 'public' ? 'primary' : 'action'} sx={{ fontSize: 40, mb: 1 }} />
                <Typography variant="body1" fontWeight={privacySettings.profileVisibility === 'public' ? 'bold' : 'normal'}>
                  Public
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={4}>
              <Paper 
                elevation={privacySettings.profileVisibility === 'friends' ? 3 : 1}
                sx={{ 
                  p: 2, 
                  textAlign: 'center',
                  cursor: 'pointer',
                  bgcolor: privacySettings.profileVisibility === 'friends' ? 'rgba(25, 118, 210, 0.1)' : 'transparent',
                  borderColor: privacySettings.profileVisibility === 'friends' ? 'primary.main' : 'transparent',
                  borderWidth: 1,
                  borderStyle: 'solid'
                }}
                onClick={() => handleSettingChange('profileVisibility', 'friends')}
              >
                <Person color={privacySettings.profileVisibility === 'friends' ? 'primary' : 'action'} sx={{ fontSize: 40, mb: 1 }} />
                <Typography variant="body1" fontWeight={privacySettings.profileVisibility === 'friends' ? 'bold' : 'normal'}>
                  Friends
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={4}>
              <Paper 
                elevation={privacySettings.profileVisibility === 'private' ? 3 : 1}
                sx={{ 
                  p: 2, 
                  textAlign: 'center',
                  cursor: 'pointer',
                  bgcolor: privacySettings.profileVisibility === 'private' ? 'rgba(25, 118, 210, 0.1)' : 'transparent',
                  borderColor: privacySettings.profileVisibility === 'private' ? 'primary.main' : 'transparent',
                  borderWidth: 1,
                  borderStyle: 'solid'
                }}
                onClick={() => handleSettingChange('profileVisibility', 'private')}
              >
                <VisibilityOff color={privacySettings.profileVisibility === 'private' ? 'primary' : 'action'} sx={{ fontSize: 40, mb: 1 }} />
                <Typography variant="body1" fontWeight={privacySettings.profileVisibility === 'private' ? 'bold' : 'normal'}>
                  Private
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </FormControl>
        
        <Divider sx={{ my: 2 }} />
        
        {/* More controls here... */}
        
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Button 
            variant="outlined" 
            color="error"
            startIcon={<Delete />}
            onClick={requestDataDeletion}
          >
            Request Data Deletion
          </Button>
        </Box>
      </Paper>
      
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
            <DataUsage sx={{ mr: 1 }} /> Recent Data Access
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          {dataUsageHistory.length > 0 ? (
            <Box>
              {dataUsageHistory.map((item, index) => (
                <Paper key={index} sx={{ p: 2, mb: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="subtitle1">{item.action}</Typography>
                    <Chip 
                      label={item.accessType} 
                      color={item.accessType === 'read' ? 'info' : 'warning'} 
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Data: {item.dataType} • Purpose: {item.purpose}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {new Date(item.timestamp).toLocaleString()}
                  </Typography>
                </Paper>
              ))}
            </Box>
          ) : (
            <Typography variant="body1">No recent data access to show.</Typography>
          )}
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default PrivacyDashboard;