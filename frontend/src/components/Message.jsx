import React, { useState } from 'react';

function Message({ message }) {
  const [expanded, setExpanded] = useState(false);

  if (message.type === 'user') {
    return (
      <div className="message-row user-row">
        <div className="message-bubble user-bubble">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.type === 'assistant') {
    return (
      <div className="message-row assistant-row">
        <div className="message-bubble assistant-bubble">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.type === 'agent') {
    return (
      <div className="message-row agent-row">
        <div className="agent-bubble">
          <div 
            className="agent-header"
            onClick={() => setExpanded(!expanded)}
          >
            <span className="agent-icon">{message.icon}</span>
            <span className="agent-name">{message.agent}</span>
            <span className="agent-tokens">{message.tokens} tokens</span>
            <span className="expand-btn">{expanded ? '▼' : '▶'}</span>
          </div>
          {expanded && (
            <div className="agent-content">
              <pre>{message.text}</pre>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (message.type === 'error') {
    return (
      <div className="message-row error-row">
        <div className="message-bubble error-bubble">
          {message.text}
        </div>
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
          </div>
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
