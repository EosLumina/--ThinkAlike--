import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import './EosLuminaGuide.css';
import { fetchGuideResponse } from '../../services/guideService';
import { useVoiceSynthesis } from '../../hooks/useVoiceSynthesis';
import { useContributorProfile } from '../../hooks/useContributorProfile';
import GuideAvatar from './GuideAvatar';
import MessageList from './MessageList';
import InputArea from './InputArea';
import VoiceControls from './VoiceControls';
import TaskRecommendations from './TaskRecommendations';

/**
 * EosLuminaGuide Component - The AI guide for ThinkAlike contributors
 * 
 * This component implements the Eos Lumina∴ "Queen Bee" persona that guides
 * contributors through the project using both text and voice interaction.
 * It embodies the project's ethical principles and helps contributors find
 * appropriate tasks based on their skills and interests.
 */
const EosLuminaGuide = ({ 
  initialMessage = "Welcome to ThinkAlike. I am Eos Lumina∴, your guide to this collective endeavor.",
  showTaskRecommendations = true,
  enableVoice = true,
  minimized = false
}) => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isMinimized, setIsMinimized] = useState(minimized);
  const [voiceEnabled, setVoiceEnabled] = useState(enableVoice);
  const messageEndRef = useRef(null);
  
  const { speak, isSpeaking, stopSpeaking, voiceSettings, updateVoiceSettings } = useVoiceSynthesis();
  const { profile, updateProfile } = useContributorProfile();

  // Initialize with welcome message
  useEffect(() => {
    if (initialMessage) {
      const welcomeMessage = {
        id: 'welcome',
        text: initialMessage,
        sender: 'guide',
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
      
      if (voiceEnabled) {
        speak(initialMessage);
      }
    }
  }, [initialMessage, voiceEnabled, speak]);

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle sending a new message
  const handleSendMessage = async (text) => {
    if (!text.trim()) return;
    
    // Add user message to state
    const userMessage = {
      id: `user-${Date.now()}`,
      text,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    
    try {
      // Get response from the guide service
      const response = await fetchGuideResponse(text, {
        conversationHistory: messages,
        contributorProfile: profile
      });
      
      const guideMessage = {
        id: `guide-${Date.now()}`,
        text: response.text,
        sender: 'guide',
        timestamp: new Date().toISOString(),
        recommendations: response.recommendations || []
      };
      
      setMessages(prev => [...prev, guideMessage]);
      
      // Update profile if guide detected new information
      if (response.profileUpdates) {
        updateProfile(response.profileUpdates);
      }
      
      // Speak the response if voice is enabled
      if (voiceEnabled) {
        speak(response.text, {
          emotion: response.emotion || 'neutral'
        });
      }
    } catch (error) {
      console.error("Error getting guide response:", error);
      
      // Add error message
      const errorMessage = {
        id: `error-${Date.now()}`,
        text: "I apologize, but I'm having trouble connecting to the hive mind. Please try again in a moment.",
        sender: 'guide',
        timestamp: new Date().toISOString(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Toggle voice functionality
  const toggleVoice = () => {
    if (isSpeaking) {
      stopSpeaking();
    }
    setVoiceEnabled(!voiceEnabled);
  };

  // Toggle minimized state
  const toggleMinimized = () => {
    setIsMinimized(!isMinimized);
    if (isSpeaking && !isMinimized) {
      stopSpeaking();
    }
  };
  
  // Get task recommendations based on profile and conversation
  const getRecommendedTasks = () => {
    // Extract recommendations from the last guide message
    const lastGuideMessage = [...messages]
      .reverse()
      .find(msg => msg.sender === 'guide' && msg.recommendations);
      
    return lastGuideMessage?.recommendations || [];
  };

  return (
    <div className={`eos-lumina-guide ${isMinimized ? 'minimized' : ''}`}>
      <div className="guide-header">
        <GuideAvatar isSpeaking={isSpeaking} />
        <h3>Eos Lumina∴</h3>
        <div className="guide-controls">
          <button 
            onClick={toggleVoice} 
            title={voiceEnabled ? "Disable voice" : "Enable voice"}
            aria-label={voiceEnabled ? "Disable voice" : "Enable voice"}
            className={`voice-toggle ${voiceEnabled ? 'active' : ''}`}
          >
            {voiceEnabled ? '🔊' : '🔇'}
          </button>
          <button 
            onClick={toggleMinimized}
            title={isMinimized ? "Expand" : "Minimize"}
            aria-label={isMinimized ? "Expand" : "Minimize"}
          >
            {isMinimized ? '▲' : '▼'}
          </button>
        </div>
      </div>
      
      {!isMinimized && (
        <>
          <div className="guide-conversation">
            <MessageList 
              messages={messages} 
              isTyping={isTyping} 
            />
            <div ref={messageEndRef} />
          </div>
          
          {showTaskRecommendations && (
            <TaskRecommendations tasks={getRecommendedTasks()} />
          )}
          
          {voiceEnabled && (
            <VoiceControls 
              isSpeaking={isSpeaking}
              onStop={stopSpeaking}
              settings={voiceSettings}
              onSettingsChange={updateVoiceSettings}
            />
          )}
          
          <InputArea 
            onSendMessage={handleSendMessage} 
            disabled={isTyping}
            placeholder="Ask me about ThinkAlike or how you can contribute..."
          />
        </>
      )}
    </div>
  );
};

EosLuminaGuide.propTypes = {
  initialMessage: PropTypes.string,
  showTaskRecommendations: PropTypes.bool,
  enableVoice: PropTypes.bool,
  minimized: PropTypes.bool
};

export default EosLuminaGuide;
