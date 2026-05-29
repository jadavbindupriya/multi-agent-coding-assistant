import React, { useState } from 'react';
import Message from './Message';
import InputBox from './InputBox';

function ChatInterface({ messages, onSubmit, loading, messagesEndRef }) {
  const [language, setLanguage] = useState('python');

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}
        {loading && (
          <div className="loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Agents are working on your task...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputBox 
        onSubmit={onSubmit}
        loading={loading}
        language={language}
        setLanguage={setLanguage}
      />
    </div>
  );
}

export default ChatInterface;
