import React, { useState, useRef, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import KnowledgePanel from './components/KnowledgePanel';
import AnalyticsPanel from './components/AnalyticsPanel';
import { solveTask } from './services/api';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 0,
      type: 'assistant',
      text: 'Hi! 👋 I\'m your Multi-Agent Coding Assistant with RAG, tool calling, MCP integrations, enhanced testing, and analytics. Upload coding standards in the Knowledge panel, then submit a task!',
      timestamp: new Date()
    }
  ]);

  const [loading, setLoading] = useState(false);
  const [activePanel, setActivePanel] = useState(null);
  const [useKnowledge, setUseKnowledge] = useState(true);
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
      const response = await solveTask(task, language, { useKnowledge });

      const agentIcons = { Planner: '📍', Coder: '💻', Reviewer: '🔍', Tester: '🧪' };
      let nextId = messages.length + 1;

      for (const agent of response.agent_outputs) {
        const agentMessage = {
          id: nextId++,
          type: 'agent',
          agent: agent.agent_name,
          icon: agentIcons[agent.agent_name] || '🤖',
          text: agent.output,
          tokens: agent.tokens_used,
          executionTime: agent.execution_time,
          toolCalls: agent.tool_calls,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, agentMessage]);
      }

      const summaryMessage = {
        id: nextId,
        type: 'summary',
        taskId: response.task_id,
        totalTokens: response.total_tokens_used,
        confidence: response.confidence_score,
        executionTime: response.execution_time,
        estimatedCost: response.estimated_cost_usd,
        knowledgeUsed: response.knowledge_used,
        solution: response.solution,
        tests: response.tests,
        testExecution: response.test_execution,
        coverage: response.coverage,
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

  const togglePanel = (panel) => {
    setActivePanel(activePanel === panel ? null : panel);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 Multi-Agent Coding Assistant</h1>
        <p>Planner • Coder • Reviewer • Tester | RAG • Tools • MCP • Analytics</p>
        <div className="header-actions">
          <button
            className={`header-btn ${activePanel === 'knowledge' ? 'active' : ''}`}
            onClick={() => togglePanel('knowledge')}
          >
            📚 Knowledge
          </button>
          <button
            className={`header-btn ${activePanel === 'analytics' ? 'active' : ''}`}
            onClick={() => togglePanel('analytics')}
          >
            📊 Analytics
          </button>
          <label className="knowledge-toggle">
            <input
              type="checkbox"
              checked={useKnowledge}
              onChange={(e) => setUseKnowledge(e.target.checked)}
            />
            Use RAG
          </label>
        </div>
      </header>

      <div className="main-content">
        {activePanel === 'knowledge' && (
          <KnowledgePanel onClose={() => setActivePanel(null)} />
        )}
        {activePanel === 'analytics' && (
          <AnalyticsPanel onClose={() => setActivePanel(null)} />
        )}

        <ChatInterface
          messages={messages}
          onSubmit={handleSubmit}
          loading={loading}
          messagesEndRef={messagesEndRef}
        />
      </div>

      <footer className="app-footer">
        <p>Powered by FastAPI + React | OpenAI GPT-4 | ChromaDB | MCP</p>
      </footer>
    </div>
  );
}

export default App;
