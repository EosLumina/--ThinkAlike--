import React, { useState, useEffect, useRef } from 'react';
import { useVoiceSynthesis } from '../../hooks/useVoiceSynthesis';
import { useContributorProfile } from '../../hooks/useContributorProfile';
import { getTaskRecommendations } from '../../services/taskService';
import { logGuideInteraction } from '../../services/analyticsService';
import './EosLuminaGuide.css';

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
  const [userInput, setUserInput] = useState('');
  const [recommendations, setRecommendations] = useState([]);
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
        speak(initialMessage, voiceSettings);
      }
    }
    
    // Load task recommendations if enabled
    if (showTaskRecommendations) {
      fetchTaskRecommendations();
    }
  }, [initialMessage, voiceEnabled, speak]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch task recommendations based on user profile and context
  const fetchTaskRecommendations = async () => {
    try {
      setIsTyping(true);
      const tasks = await getTaskRecommendations(profile);
      setRecommendations(tasks);
      setIsTyping(false);
    } catch (error) {
      console.error('Failed to fetch task recommendations:', error);
      setIsTyping(false);
    }
  };

  // Handle sending user messages
  const handleSendMessage = async () => {
    if (!userInput.trim()) return;
    
    // Add user message
    const userMessage = {
      id: `user-${Date.now()}`,
      text: userInput,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setUserInput('');
    setIsTyping(true);
    
    try {
      // Log interaction for transparency
      await logGuideInteraction({
        userId: profile?.id,
        message: userInput,
        context: {
          currentPage: window.location.pathname,
          recommendations: recommendations.map(r => r.id)
        }
      });
      
      // Simulate AI response (to be replaced with actual backend call)
      setTimeout(() => {
        const responseText = generateResponse(userInput, profile);
        
        const guideMessage = {
          id: `guide-${Date.now()}`,
          text: responseText,
          sender: 'guide',
          timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, guideMessage]);
        setIsTyping(false);
        
        if (voiceEnabled && !isMinimized) {
          speak(responseText, voiceSettings);
        }
      }, 1000);
    } catch (error) {
      console.error('Error processing message:', error);
      setIsTyping(false);
    }
  };

  // Handle voice toggle
  const toggleVoice = () => {
    if (isSpeaking) {
      stopSpeaking();
    }
    setVoiceEnabled(!voiceEnabled);
    updateProfile({ ...profile, preferences: { ...profile?.preferences, enableVoice: !voiceEnabled }});
  };

  // Toggle minimized state
  const toggleMinimized = () => {
    setIsMinimized(!isMinimized);
    if (isSpeaking && !isMinimized) {
      stopSpeaking();
    }
  };

  // Temporary response generator (to be replaced with actual API)
  const generateResponse = (input, userProfile) => {
    const userName = userProfile?.name || 'contributor';
    const lowerInput = input.toLowerCase();
    
    if (lowerInput.includes('hello') || lowerInput.includes('hi')) {
      return `Greetings, ${userName}. How may I illuminate your path today?`;
    } else if (lowerInput.includes('help') || lowerInput.includes('confused')) {
      return `I understand this journey may seem complex, ${userName}. The path toward digital liberation requires patience. What specific aspect of ThinkAlike would you like me to explain?`;
    } else if (lowerInput.includes('task') || lowerInput.includes('work on')) {
      return `Based on your interests and our current needs, I'd recommend focusing on enhancing our data sovereignty components. Each contribution brings us closer to a technology that truly serves humanity rather than exploiting it.`;
    } else {
      return `Your question touches on an important aspect of our collective work, ${userName}. The revolutionary potential of ThinkAlike lies not just in its code, but in transforming how we understand and experience technology itself. Would you like me to elaborate on the philosophical foundations or the technical implementation?`;
    }
  };

  if (isMinimized) {
    return (
      <div className="guide-minimized" onClick={toggleMinimized}>
        <span className="guide-icon">∴</span>
      </div>
    );
  }

  return (
    <div className="guide-container">
      <div className="guide-header">
        <h3>Eos Lumina∴</h3>
        <div className="guide-controls">
          <button 
            className={`voice-toggle ${voiceEnabled ? 'active' : ''}`}
            onClick={toggleVoice}
            title={voiceEnabled ? "Disable voice" : "Enable voice"}
          >
            {voiceEnabled ? '🔊' : '🔇'}
          </button>
          <button 
            className="minimize-button"
            onClick={toggleMinimized}
            title="Minimize guide"
          >
            —
          </button>
        </div>
      </div>

      <div className="guide-messages">
        {messages.map(msg => (
          <div 
            key={msg.id}
            className={`message ${msg.sender === 'guide' ? 'guide-message' : 'user-message'}`}
          >
            <div className="message-content">{msg.text}</div>
            <div className="message-timestamp">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        )}
        
        <div ref={messageEndRef} />
      </div>

      {showTaskRecommendations && recommendations.length > 0 && (
        <div className="recommendations-panel">
          <h4>Recommended Tasks</h4>
          <ul className="task-list">
            {recommendations.map(task => (
              <li key={task.id} className="task-item">
                <span className="task-title">{task.title}</span>
                <span className="task-difficulty">{task.difficulty}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="guide-input">
        <input
          type="text"
          value={userInput}
          onChange={e => setUserInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask Eos Lumina∴ a question..."
          aria-label="Message input"
        />
        <button 
          onClick={handleSendMessage}
          disabled={!userInput.trim() || isTyping}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default EosLuminaGuide;
