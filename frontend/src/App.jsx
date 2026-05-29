import React, { useState } from 'react';
import TaskForm from './components/TaskForm';
import AgentOutput from './components/AgentOutput';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (task, language) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const { solveTask } = await import('./services/api');
      const response = await solveTask(task, language);
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to solve task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 Multi-Agent Coding Assistant</h1>
        <p>Planner → Coder → Reviewer → Tester</p>
      </header>

      <main className="app-main">
        <TaskForm onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="error-box">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading-box">
            <div className="spinner"></div>
            <p>Running agents... This may take 30-60 seconds</p>
          </div>
        )}

        {result && !loading && (
          <AgentOutput result={result} />
        )}
      </main>

      <footer className="app-footer">
        <p>Backend: http://localhost:8000 | Frontend: React 18</p>
      </footer>
    </div>
  );
}

export default App;