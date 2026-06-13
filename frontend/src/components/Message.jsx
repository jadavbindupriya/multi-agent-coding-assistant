import React, { useState } from 'react';

function Message({ message }) {
  const [expanded, setExpanded] = useState(false);

  if (message.type === 'user') {
    return (
      <div className="message-row user-row">
        <div className="message-bubble user-bubble">{message.text}</div>
      </div>
    );
  }

  if (message.type === 'assistant') {
    return (
      <div className="message-row assistant-row">
        <div className="message-bubble assistant-bubble">{message.text}</div>
      </div>
    );
  }

  if (message.type === 'agent') {
    return (
      <div className="message-row agent-row">
        <div className="agent-bubble">
          <div className="agent-header" onClick={() => setExpanded(!expanded)}>
            <span className="agent-icon">{message.icon}</span>
            <span className="agent-name">{message.agent}</span>
            <span className="agent-tokens">{message.tokens} tokens</span>
            {message.executionTime && (
              <span className="agent-time">{message.executionTime}s</span>
            )}
            <span className="expand-btn">{expanded ? '▼' : '▶'}</span>
          </div>
          {expanded && (
            <div className="agent-content">
              <pre>{message.text}</pre>
              {message.toolCalls?.length > 0 && (
                <div className="tool-calls">
                  <strong>🔧 Tools used:</strong>
                  {message.toolCalls.map((tc, i) => (
                    <div key={i} className="tool-call">
                      {tc.tool}: {tc.result?.substring(0, 120)}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  if (message.type === 'error') {
    return (
      <div className="message-row error-row">
        <div className="message-bubble error-bubble">{message.text}</div>
      </div>
    );
  }

  if (message.type === 'summary') {
    return (
      <div className="message-row summary-row">
        <div className="summary-bubble">
          <h3>✅ Task Complete!</h3>
          <div className="summary-info">
            <p><strong>Task ID:</strong> {message.taskId}</p>
            <p><strong>Total Tokens:</strong> {message.totalTokens}</p>
            <p><strong>Confidence:</strong> {(message.confidence * 100).toFixed(0)}%</p>
            <p><strong>Time:</strong> {message.executionTime}s</p>
            {message.estimatedCost > 0 && (
              <p><strong>Est. Cost:</strong> ${message.estimatedCost.toFixed(4)}</p>
            )}
            {message.knowledgeUsed && <p><strong>RAG:</strong> Knowledge base consulted</p>}
          </div>

          {message.testExecution && (
            <div className="test-results">
              <p>
                <strong>Tests:</strong>{' '}
                {message.testExecution.passed ? '✅ PASSED' : '❌ FAILED'}{' '}
                ({message.testExecution.passed_count}/{message.testExecution.total})
              </p>
              {message.testExecution.edge_cases_found?.length > 0 && (
                <p><strong>Edge cases:</strong> {message.testExecution.edge_cases_found.join(', ')}</p>
              )}
            </div>
          )}

          {message.coverage && (
            <div className="coverage-bar-container">
              <p><strong>Coverage:</strong> {(message.coverage.coverage_percent * 100).toFixed(0)}%</p>
              <div className="coverage-bar">
                <div
                  className="coverage-fill"
                  style={{ width: `${message.coverage.coverage_percent * 100}%` }}
                />
              </div>
            </div>
          )}

          <details>
            <summary>Final Solution</summary>
            <pre>{message.solution}</pre>
          </details>
          <details>
            <summary>Test Cases</summary>
            <pre>{message.tests}</pre>
          </details>
        </div>
      </div>
    );
  }

  return null;
}

export default Message;
