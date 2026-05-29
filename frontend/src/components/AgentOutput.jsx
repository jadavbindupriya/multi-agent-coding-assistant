import React, { useState } from 'react';

function AgentOutput({ result }) {
  const [expandedAgent, setExpandedAgent] = useState(0);

  const agents = [
    { name: 'Planner', icon: '📍', color: '#FF6B6B' },
    { name: 'Coder', icon: '💻', color: '#4ECDC4' },
    { name: 'Reviewer', icon: '🔍', color: '#FFE66D' },
    { name: 'Tester', icon: '🧪', color: '#95E1D3' }
  ];

  return (
    <div className="agent-output">
      <div className="result-summary">
        <h2>✅ Task Completed!</h2>
        <div className="task-info">
          <p><strong>Task ID:</strong> {result.task_id}</p>
          <p><strong>Tokens Used:</strong> {result.total_tokens_used}</p>
          <p><strong>Confidence:</strong> {(result.confidence_score * 100).toFixed(0)}%</p>
        </div>
      </div>

      <div className="agents-grid">
        {result.agent_outputs.map((agent, index) => (
          <div key={index} className="agent-card">
            <div
              className="agent-header"
              onClick={() => setExpandedAgent(expandedAgent === index ? -1 : index)}
              style={{ borderLeft: `4px solid ${agents[index].color}` }}
            >
              <span className="agent-icon">{agents[index].icon}</span>
              <span className="agent-name">{agent.agent_name}</span>
              <span className="agent-tokens">{agent.tokens_used} tokens</span>
              <span className="expand-icon">
                {expandedAgent === index ? '▼' : '▶'}
              </span>
            </div>

            {expandedAgent === index && (
              <div className="agent-content">
                <pre>{agent.output}</pre>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="solution-box">
        <h3>📝 Final Solution</h3>
        <pre>{result.solution}</pre>
      </div>
    </div>
  );
}

export default AgentOutput;