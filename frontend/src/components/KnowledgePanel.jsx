import React, { useState, useEffect } from 'react';
import { uploadDocument, listDocuments, getKnowledgeStatus } from '../services/api';

function KnowledgePanel({ onClose }) {
  const [documents, setDocuments] = useState([]);
  const [status, setStatus] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const refresh = async () => {
    try {
      const [docs, stat] = await Promise.all([listDocuments(), getKnowledgeStatus()]);
      setDocuments(docs);
      setStatus(stat);
    } catch (err) {
      setMessage(`Error: ${err.message}`);
    }
  };

  useEffect(() => { refresh(); }, []);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setMessage('');
    try {
      const result = await uploadDocument(file);
      setMessage(`✅ ${result.message}`);
      refresh();
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  return (
    <div className="side-panel">
      <div className="panel-header">
        <h3>📚 Knowledge Base</h3>
        <button className="panel-close" onClick={onClose}>✕</button>
      </div>
      <div className="panel-body">
        <p className="panel-desc">
          Upload coding standards, docs (.pdf, .txt, .md). Agents search this before solving.
        </p>

        <label className="upload-btn">
          {uploading ? 'Uploading...' : '📄 Upload Document'}
          <input type="file" accept=".pdf,.txt,.md" onChange={handleUpload} disabled={uploading} hidden />
        </label>

        {message && <p className="panel-message">{message}</p>}

        {status && (
          <div className="panel-stat">
            <span>{status.document_count} documents</span>
            <span>{status.total_chunks} chunks</span>
          </div>
        )}

        {documents.length > 0 && (
          <ul className="doc-list">
            {documents.map((doc) => (
              <li key={doc.source}>
                <span className="doc-name">{doc.source}</span>
                <span className="doc-chunks">{doc.chunks} chunks</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default KnowledgePanel;
