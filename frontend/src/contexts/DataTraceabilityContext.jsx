import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const DataTraceabilityContext = createContext();

export const useDataTraceability = () => useContext(DataTraceabilityContext);

/**
 * DataTraceabilityProvider - Core component for ThinkAlike's ethical data handling
 * 
 * This provider implements transparent data usage tracking and user controls,
 * allowing users to see how their data is being used throughout the application.
 */
export const DataTraceabilityProvider = ({ children }) => {
  const [dataUsageHistory, setDataUsageHistory] = useState([]);
  const [isHistoryLoaded, setIsHistoryLoaded] = useState(false);
  const [dataPreferences, setDataPreferences] = useState({
    allowAnalytics: true,
    allowMatching: true,
    allowLocationSharing: false,
    allowThirdPartySharing: false,
    minimizeDataCollection: false
  });
  
  const { token, isAuthenticated } = useAuth();
  
  // Fetch data usage history when authenticated
  useEffect(() => {
    if (isAuthenticated && token && !isHistoryLoaded) {
      fetchDataUsageHistory();
      fetchDataPreferences();
    }
  }, [isAuthenticated, token]);
  
  // Track data usage
  const trackDataUsage = async (usageData) => {
    try {
      // Add timestamp
      const usage = {
        ...usageData,
        timestamp: new Date().toISOString()
      };
      
      // Record locally for immediate feedback
      setDataUsageHistory(prev => [usage, ...prev]);
      
      // Send to backend if authenticated
      if (isAuthenticated && token) {
        await axios.post('/api/v1/data-traceability/track', usage, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      
      return true;
    } catch (error) {
      console.error('Error tracking data usage:', error);
      return false;
    }
  };
  
  // Fetch usage history from the backend
  const fetchDataUsageHistory = async () => {
    try {
      const response = await axios.get('/api/v1/data-traceability/history', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setDataUsageHistory(response.data);
      setIsHistoryLoaded(true);
    } catch (error) {
      console.error('Error fetching data usage history:', error);
    }
  };
  
  // Fetch user data preferences
  const fetchDataPreferences = async () => {
    try {
      const response = await axios.get('/api/v1/data-traceability/preferences', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setDataPreferences(response.data);
    } catch (error) {
      console.error('Error fetching data preferences:', error);
    }
  };
  
  // Update user data preferences
  const updateDataPreferences = async (newPreferences) => {
    try {
      await axios.put('/api/v1/data-traceability/preferences', newPreferences, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setDataPreferences(newPreferences);
      return true;
    } catch (error) {
      console.error('Error updating data preferences:', error);
      return false;
    }
  };
  
  // Request data deletion (GDPR compliance)
  const requestDataDeletion = async (dataCategories) => {
    try {
      const response = await axios.post('/api/v1/data-traceability/delete-request', 
        { categories: dataCategories },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      
      return {
        success: true,
        requestId: response.data.requestId
      };
    } catch (error) {
      console.error('Error requesting data deletion:', error);
      return { success: false };
    }
  };
  
  // Download personal data (GDPR compliance)
  const downloadPersonalData = async () => {
    try {
      const response = await axios.get('/api/v1/data-traceability/download', {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'ThinkAlike-PersonalData.json');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading personal data:', error);
      return { success: false };
    }
  };
  
  // Check if a specific data usage is allowed by user preferences
  const isDataUsageAllowed = (usageType) => {
    switch (usageType) {
      case 'analytics':
        return dataPreferences.allowAnalytics;
      case 'matching':
        return dataPreferences.allowMatching;
      case 'location':
        return dataPreferences.allowLocationSharing;
      case 'third_party':
        return dataPreferences.allowThirdPartySharing;
      default:
        return true;
    }
  };
  
  // Context value
  const value = {
    dataUsageHistory,
    dataPreferences,
    trackDataUsage,
    updateDataPreferences,
    requestDataDeletion,
    downloadPersonalData,
    isDataUsageAllowed,
    refreshHistory: fetchDataUsageHistory
  };
  
  return (
    <DataTraceabilityContext.Provider value={value}>
      {children}
    </DataTraceabilityContext.Provider>
  );
};