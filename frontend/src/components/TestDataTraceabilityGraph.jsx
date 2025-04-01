import React, { useState } from 'react';
import DataTraceabilityGraph from './DataTraceabilityGraph';

function TestDataTraceabilityGraph() {
  const [apiStatus, setApiStatus] = useState('idle');
  const [requestData] = useState({
    query: "What's the weather today?",
    options: { detailed: true },
    timestamp: new Date().toISOString()
  });
  const [responseData, setResponseData] = useState({});
  const [statusCode, setStatusCode] = useState(0);

  // Simulate an API call
  const simulateApiCall = () => {
    // Step 1: Set loading state
    setApiStatus('loading');

    // Step 2: After 1.5 seconds, simulate success response
    setTimeout(() => {
      if (Math.random() > 0.2) { // 80% success chance
        setApiStatus('success');
        setStatusCode(200);
        setResponseData({
          temperature: 72,
          condition: "Sunny",
          forecast: [
            { day: "Today", high: 75, low: 65, condition: "Clear" },
            { day: "Tomorrow", high: 70, low: 60, condition: "Partly Cloudy" },
            { day: "Wednesday", high: 68, low: 58, condition: "Rain" }
          ],
          location: "New York, NY",
          timestamp: new Date().toISOString()
        });
      } else {
        // Simulate error
        setApiStatus('error');
        setStatusCode(500);
        setResponseData({
          error: "Internal Server Error",
          message: "Weather service unavailable"
        });
      }
    }, 1500);
  };

  const resetDemo = () => {
    setApiStatus('idle');
    setResponseData({});
    setStatusCode(0);
  };

  return (
    <div style={{ padding: '20px', background: '#111', color: 'white', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Data Traceability Graph Demo</h1>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        marginBottom: '30px',
        gap: '20px'
      }}>
        <button
          onClick={simulateApiCall}
          disabled={apiStatus === 'loading'}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: apiStatus === 'loading' ? '#555' : '#F86B03',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: apiStatus === 'loading' ? 'not-allowed' : 'pointer'
          }}
        >
          {apiStatus === 'loading' ? 'Loading...' : 'Simulate API Call'}
        </button>

        <button
          onClick={resetDemo}
          disabled={apiStatus === 'idle' || apiStatus === 'loading'}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: (apiStatus === 'idle' || apiStatus === 'loading') ? '#555' : '#800000',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: (apiStatus === 'idle' || apiStatus === 'loading') ? 'not-allowed' : 'pointer'
          }}
        >
          Reset Demo
        </button>
      </div>

      <div style={{ marginBottom: '20px', textAlign: 'center' }}>
        <div style={{
          display: 'inline-block',
          padding: '10px 15px',
          borderRadius: '4px',
          backgroundColor:
            apiStatus === 'idle' ? '#555' :
            apiStatus === 'loading' ? '#FFC300' :
            apiStatus === 'success' ? '#28a745' : '#dc3545',
          color: 'white',
          fontWeight: 'bold'
        }}>
          Status: {apiStatus.toUpperCase()}
          {statusCode > 0 && (' (' + statusCode + ')')}
        </div>
      </div>

      <DataTraceabilityGraph
        apiEndpoint="https://api.thinkalike.com/weather"
        method="GET"
        requestData={requestData}
        responseData={responseData}
        statusCode={statusCode}
        status={apiStatus}
        validationPassed={apiStatus === 'success'}
        validationMessage={apiStatus === 'error' ? "Failed to validate response data" : ""}
        title="Weather API Data Flow"
      />
    </div>
  );
}

export default TestDataTraceabilityGraph;
