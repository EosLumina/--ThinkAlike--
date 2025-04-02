import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';
import { useDataTraceability } from '../../contexts/DataTraceabilityContext';
import { 
  Box, Paper, Typography, TextField, Button, Avatar, 
  Grid, Divider, FormControl, InputLabel, Select,
  MenuItem, Chip, IconButton, Alert, CircularProgress,
  FormHelperText
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { Edit, PhotoCamera } from '@mui/icons-material';

/**
 * ProfileEdit component for ThinkAlike
 * Allows user to update their profile information with transparent data handling
 */
const ProfileEdit = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    bio: '',
    birthdate: null,
    location: '',
    staticLocationCity: '',
    staticLocationCountry: '',
  });
  
  const [countries, setCountries] = useState([]);
  const [formErrors, setFormErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [profilePicture, setProfilePicture] = useState(null);
  const [profilePictureUrl, setProfilePictureUrl] = useState('');
  
  const { token, user } = useAuth();
  const { trackDataUsage } = useDataTraceability();
  const navigate = useNavigate();
  
  // Fetch profile data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/v1/profile', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Track data usage for transparency
        trackDataUsage({
          action: 'fetch_profile',
          dataType: 'profile_information',
          purpose: 'Display profile data for editing',
          accessType: 'read',
          userConsent: true
        });
        
        const profile = response.data;
        setFormData({
          fullName: user.full_name || '',
          bio: profile.bio || '',
          birthdate: profile.birthdate ? new Date(profile.birthdate) : null,
          location: profile.location || '',
          staticLocationCity: profile.static_location_city || '',
          staticLocationCountry: profile.static_location_country || '',
        });
        
        if (profile.profile_picture_url) {
          setProfilePictureUrl(profile.profile_picture_url);
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      } finally {
        setLoading(false);
      }
    };
    
    // Fetch country list for location selection
    const fetchCountries = async () => {
      try {
        // In a real app, this would fetch from an API
        // For MVP, we'll use a small hardcoded list
        setCountries([
          { code: 'US', name: 'United States' },
          { code: 'CA', name: 'Canada' },
          { code: 'UK', name: 'United Kingdom' },
          { code: 'AU', name: 'Australia' },
          { code: 'DE', name: 'Germany' },
          { code: 'FR', name: 'France' },
          { code: 'JP', name: 'Japan' },
          { code: 'BR', name: 'Brazil' },
          { code: 'IN', name: 'India' },
        ]);
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };
    
    fetchProfile();
    fetchCountries();
  }, [token, user]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear any previous error for this field
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  const handleBirthdateChange = (date) => {
    setFormData(prev => ({
      ...prev,
      birthdate: date
    }));
    
    if (formErrors.birthdate) {
      setFormErrors(prev => ({
        ...prev,
        birthdate: ''
      }));
    }
  };
  
  const handleProfilePictureChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      // Create a preview URL
      const previewUrl = URL.createObjectURL(file);
      setProfilePictureUrl(previewUrl);
      
      // Store file for upload
      setProfilePicture(file);
    }
  };
  
  const validateForm = () => {
    const errors = {};
    
    if (!formData.fullName) {
      errors.fullName = 'Name is required';
    }
    
    if (formData.bio && formData.bio.length > 500) {
      errors.bio = 'Bio must be 500 characters or less';
    }
    
    // Age validation (must be at least 18)
    if (formData.birthdate) {
      const today = new Date();
      const eighteenYearsAgo = new Date(
        today.getFullYear() - 18,
        today.getMonth(),
        today.getDate()
      );
      
      if (formData.birthdate > eighteenYearsAgo) {
        errors.birthdate = 'You must be at least 18 years old';
      }
    }
    
    if (formData.staticLocationCity && formData.staticLocationCity.length > 100) {
      errors.staticLocationCity = 'City name is too long';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      // Track data usage for transparency before update
      trackDataUsage({
        action: 'update_profile',
        dataType: 'profile_information',
        purpose: 'Save updated profile information',
        accessType: 'update',
        dataFields: Object.keys(formData),
        userConsent: true
      });
      
      // First upload profile picture if changed
      let pictureUrl = profilePictureUrl;
      if (profilePicture) {
        const pictureFormData = new FormData();
        pictureFormData.append('profilePicture', profilePicture);
        
        const uploadResponse = await axios.post('/api/v1/profile/upload-picture', 
          pictureFormData, {
            headers: { 
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        pictureUrl = uploadResponse.data.url;
      }
      
      // Then update profile data
      await axios.put('/api/v1/profile', {
        full_name: formData.fullName,
        bio: formData.bio,
        birthdate: formData.birthdate ? formData.birthdate.toISOString().split('T')[0] : null,
        location: formData.location,
        profile_picture_url: pictureUrl,
        static_location_city: formData.staticLocationCity,
        static_location_country: formData.staticLocationCountry,
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setSaveSuccess(true);
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setSaveSuccess(false);
      }, 3000);
    } catch (error) {
      console.error('Error updating profile:', error);
      setFormErrors(prev => ({
        ...prev,
        submit: 'Error saving profile. Please try again.'
      }));
    } finally {
      setLoading(false);
    }
  };
  
  if (loading && !formData.fullName) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Paper elevation={2} sx={{ p: 4, maxWidth: 800, mx: 'auto', mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Edit Your Profile
        </Typography>
        
        <Divider sx={{ mb: 3 }} />
        
        {/* Data usage transparency notice */}
        <Alert severity="info" sx={{ mb: 3 }}>
          Your profile information helps find compatible connections. You control what you share,
          and can update or remove it anytime. See our 
          <Button color="info" sx={{ textTransform: 'none' }}>Data Policy</Button> to learn more.
        </Alert>
        
        {saveSuccess && (
          <Alert severity="success" sx={{ mb: 3 }}>
            Profile updated successfully!
          </Alert>
        )}
        
        {formErrors.submit && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {formErrors.submit}
          </Alert>
        )}
        
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Profile Picture */}
            <Grid item xs={12} display="flex" justifyContent="center">
              <Box sx={{ position: 'relative' }}>
                <Avatar
                  src={profilePictureUrl}
                  alt={formData.fullName}
                  sx={{ width: 120, height: 120, mb: 2 }}
                />
                <label htmlFor="profile-picture-upload">
                  <input
                    accept="image/*"
                    id="profile-picture-upload"
                    type="file"
                    style={{ display: 'none' }}
                    onChange={handleProfilePictureChange}
                  />
                  <IconButton 
                    component="span" 
                    sx={{ 
                      position: 'absolute',
                      bottom: 10,
                      right: -10,
                      backgroundColor: 'primary.main',
                      color: 'white',
                      '&:hover': {
                        backgroundColor: 'primary.dark',
                      }
                    }}
                  >
                    <PhotoCamera />
                  </IconButton>
                </label>
              </Box>
            </Grid>
            
            {/* Full Name */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Full Name"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                error={Boolean(formErrors.fullName)}
                helperText={formErrors.fullName}
              />
            </Grid>
            
            {/* Bio */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                multiline
                rows={4}
                error={Boolean(formErrors.bio)}
                helperText={formErrors.bio || `${formData.bio?.length || 0}/500 characters`}
              />
            </Grid>
            
            {/* Birthdate */}
            <Grid item xs={12} sm={6}>
              <DatePicker
                label="Birthdate"
                value={formData.birthdate}
                onChange={handleBirthdateChange}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    error: Boolean(formErrors.birthdate),
                    helperText: formErrors.birthdate,
                  },
                }}
              />
            </Grid>
            
            {/* Location */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., New York, NY"
              />
            </Grid>
            
            {/* City */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="City"
                name="staticLocationCity"
                value={formData.staticLocationCity}
                onChange={handleChange}
                error={Boolean(formErrors.staticLocationCity)}
                helperText={formErrors.staticLocationCity}
              />
            </Grid>
            
            {/* Country */}
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel id="country-label">Country</InputLabel>
                <Select
                  labelId="country-label"
                  name="staticLocationCountry"
                  value={formData.staticLocationCountry}
                  onChange={handleChange}
                  label="Country"
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  {countries.map((country) => (
                    <MenuItem key={country.code} value={country.name}>
                      {country.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            {/* Action Buttons */}
            <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
              <Button 
                variant="outlined" 
                color="secondary"
                onClick={() => navigate('/profile')}
              >
                Cancel
              </Button>
              <Button 
                type="submit" 
                variant="contained" 
                color="primary"
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Save Profile'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </LocalizationProvider>
  );
};

export default ProfileEdit;