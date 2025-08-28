import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState<string>('Checking...')

  useEffect(() => {
    // Check backend connection
    fetch('/api/health')
      .then(res => res.json())
      .then(data => {
        setBackendStatus(`✅ Backend: ${data.status}`)
      })
      .catch(err => {
        setBackendStatus(`❌ Backend: Disconnected`)
        console.error('Backend connection failed:', err)
      })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI-Powered POS Account Hierarchy</h1>
        <p>
          Autonomous agent for processing inconsistent customer names into structured account hierarchies
        </p>
        <div className="status">
          <p>{backendStatus}</p>
        </div>
        <div className="features">
          <h2>Core Features (In Development)</h2>
          <ul>
            <li>📊 POS Report File Upload</li>
            <li>🔍 AI Classification Agent</li>
            <li>🏢 Account Hierarchy Management</li>
            <li>📈 Role-based Reporting Dashboards</li>
          </ul>
        </div>
      </header>
    </div>
  )
}

export default App
