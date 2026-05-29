import React, { useState, useRef, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import { solveTask } from './services/api';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 0,
      type: 'assistant',
      text: 'Hi! 👋 I\'m your Multi-Agent Coding Assistant. Submit a coding task and I\'ll break it down, write the code, review it, and create tests. What would you like me to build?',
      timestamp: new Date()
    }
  ]);
  
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (task, language) => {
    const userMessage = {
      id: messages.length,
      type: 'user',
      text: task,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await solveTask(task, language);

      const planMessage = {
        id: messages.length + 1,
        type: 'agent',
        agent: 'Planner',
        icon: '📍',
        text: response.agent_outputs[0].output,
        tokens: response.agent_outputs[0].tokens_used,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, planMessage]);

      const codeMessage = {
        id: messages.length + 2,
        type: 'agent',
        agent: 'Coder',
        icon: '💻',
        text: response.agent_outputs[1].output,
        tokens: response.agent_outputs[1].tokens_used,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, codeMessage]);

      const reviewMessage = {
        id: messages.length + 3,
        type: 'agent',
        agent: 'Reviewer',
        icon: '🔍',
        text: response.agent_outputs[2].output,
        tokens: response.agent_outputs[2].tokens_used,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, reviewMessage]);

      const testMessage = {
        id: messages.length + 4,
        type: 'agent',
        agent: 'Tester',
        icon: '🧪',
        text: response.agent_outputs[3].output,
        tokens: response.agent_outputs[3].tokens_used,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, testMessage]);

      const summaryMessage = {
        id: messages.length + 5,
        type: 'summary',
        taskId: response.task_id,
        totalTokens: response.total_tokens_used,
        confidence: response.confidence_score,
        solution: response.solution,
        tests: response.tests,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, summaryMessage]);

    } catch (err) {
      const errorMessage = {
        id: messages.length + 1,
        type: 'error',
        text: `❌ Error: ${err.message || 'Failed to process task'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 Multi-Agent Coding Assistant</h1>
        <p>Planner • Coder • Reviewer • Tester</p>
      </header>

      <ChatInterface 
        messages={messages} 
        onSubmit={handleSubmit}
        loading={loading}
        messagesEndRef={messagesEndRef}
      />

      <footer className="app-footer">
        <p>Powered by FastAPI + React | OpenAI GPT-4</p>
      </footer>
    </div>
  );
}

export default App;
