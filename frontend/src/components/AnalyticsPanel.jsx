import React, { useState, useEffect } from 'react';
import { getAnalyticsSummary, getIntegrationStatus } from '../services/api';

function AnalyticsPanel({ onClose }) {
  const [analytics, setAnalytics] = useState(null);
  const [integrations, setIntegrations] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [summary, status] = await Promise.all([
          getAnalyticsSummary(),
          getIntegrationStatus(),
        ]);
        setAnalytics(summary);
        setIntegrations(status);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div className="side-panel"><p className="panel-desc">Loading analytics...</p></div>;

  return (
    <div className="side-panel">
      <div className="panel-header">
        <h3>📊 Analytics</h3>
        <button className="panel-close" onClick={onClose}>✕</button>
      </div>
      <div className="panel-body">
        {analytics && (
          <>
            <div className="metric-grid">
              <div className="metric-card">
                <span className="metric-value">{analytics.total_tasks}</span>
                <span className="metric-label">Tasks</span>
              </div>
              <div className="metric-card">
                <span className="metric-value">{analytics.total_tokens?.toLocaleString()}</span>
                <span className="metric-label">Tokens</span>
              </div>
              <div className="metric-card">
                <span className="metric-value">${analytics.total_cost_usd?.toFixed(3)}</span>
                <span className="metric-label">Est. Cost</span>
              </div>
              <div className="metric-card">
                <span className="metric-value">{analytics.avg_execution_time}s</span>
                <span className="metric-label">Avg Time</span>
              </div>
            </div>

            {analytics.agent_performance && Object.keys(analytics.agent_performance).length > 0 && (
              <div className="agent-metrics">
                <h4>Agent Performance</h4>
                {Object.entries(analytics.agent_performance).map(([name, stats]) => (
                  <div key={name} className="agent-metric-row">
                    <span className="agent-metric-name">{name}</span>
                    <span>{stats.avg_tokens} tok</span>
                    <span>{stats.avg_time}s</span>
                    {stats.failures > 0 && <span className="metric-error">{stats.failures} err</span>}
                  </div>
                ))}
              </div>
            )}

            {analytics.error_count > 0 && (
              <div className="error-summary">
                <h4>⚠️ {analytics.error_count} Errors</h4>
              </div>
            )}
          </>
        )}

        {integrations && (
          <div className="integration-status">
            <h4>🔗 Integrations</h4>
            <div className="integration-badges">
              <span className={integrations.github ? 'badge active' : 'badge'}>GitHub</span>
              <span className={integrations.slack ? 'badge active' : 'badge'}>Slack</span>
              <span className={integrations.jira ? 'badge active' : 'badge'}>Jira</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalyticsPanel;
