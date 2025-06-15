// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import JarvisTroubleshootingSystem from './components/JarvisTroubleshootingSystem';
import axios from 'axios';

function App() {
  const [systemStatus, setSystemStatus] = useState('loading');
  const [systemInfo, setSystemInfo] = useState(null);

  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get('/system-info');
      setSystemInfo(response.data);
      setSystemStatus('ready');
    } catch (error) {
      console.error('Failed to check system status:', error);
      setSystemStatus('error');
    }
  };

  if (systemStatus === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl">Initializing JARVIS System...</p>
        </div>
      </div>
    );
  }

  if (systemStatus === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-600 mb-2">System Error</h1>
          <p className="text-gray-600">Failed to connect to JARVIS backend</p>
          <button 
            onClick={checkSystemStatus}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              JARVIS Wastewater Treatment System
            </h1>
            <div className="text-sm text-gray-600">
              Status: <span className="text-green-600 font-medium">Connected</span>
              {systemInfo && (
                <span className="ml-4">
                  DB: {systemInfo.documents} documents
                </span>
              )}
            </div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6">
        <JarvisTroubleshootingSystem />
      </main>
    </div>
  );
}

export default App;