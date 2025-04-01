import React, { useState, useEffect } from 'react';
import DataTraceability from './components/DataTraceability';
//import dataFlow from './data/DataTraceabilityExampleData'; // NO LONGER NEEDED
import './App.css';

function App() {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [dataFlow, setDataFlow] = useState({ nodes: [], edges: [] }); // Initialize with empty data
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        fetch('/api/v1/graph') //  Fetch from the backend API
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setDataFlow(data); //  Update state with fetched data
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

  if (loading) {
    return <div>Loading...</div>;
  }

    if (error) {
    return <div>Error: {error}</div>
    }

  return (
    <div className="App">
      <header className="App-header">
        <h1>ThinkAlike</h1>
        <button onClick={toggleConnectionStatus}>
          Toggle Connection Status (Current: {connectionStatus})
        </button>
      </header>
      <section className="content">
        <DataTraceability dataFlow={dataFlow} connectionStatus={connectionStatus} />
      </section>
    </div>
  );
}

export default App;
