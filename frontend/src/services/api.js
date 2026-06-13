import axios from 'axios';

const API_BASE =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'development'
    ? '/api'
    : 'http://localhost:8000/api');

const handleError = (error) => {
  const status = error.response?.status;
  const detail = error.response?.data?.detail;

  if (status === 404) {
    throw new Error(
      'API not found (404). Start the backend: python scripts/run_backend.py'
    );
  }

  const message =
    typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail.map((d) => d.msg).join(', ')
        : error.response?.data?.message || error.message || 'Request failed';
  throw new Error(message);
};

export const solveTask = async (task, language = 'python', options = {}) => {
  try {
    const response = await axios.post(`${API_BASE}/solve`, {
      task,
      language,
      context: options.context || null,
      use_knowledge: options.useKnowledge !== false,
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getTaskStatus = async (taskId) => {
  try {
    const response = await axios.get(`${API_BASE}/status/${taskId}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const evaluateResponse = async (response, task, criteria) => {
  try {
    const res = await axios.post(`${API_BASE}/evaluate`, { response, task, criteria });
    return res.data;
  } catch (error) {
    handleError(error);
  }
};

// Phase 5: Knowledge Base
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post(`${API_BASE}/knowledge/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const searchKnowledge = async (query, topK = 3) => {
  try {
    const response = await axios.post(`${API_BASE}/knowledge/search`, { query, top_k: topK });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const listDocuments = async () => {
  try {
    const response = await axios.get(`${API_BASE}/knowledge/documents`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getKnowledgeStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE}/knowledge/status`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// Phase 7: Integrations
export const getIntegrationStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE}/integrations/status`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const createGitHubIssue = async (owner, repo, title, body) => {
  try {
    const response = await axios.post(`${API_BASE}/integrations/github/issue`, {
      owner, repo, title, body,
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// Phase 9: Analytics
export const getAnalyticsSummary = async () => {
  try {
    const response = await axios.get(`${API_BASE}/analytics/summary`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getRecentErrors = async () => {
  try {
    const response = await axios.get(`${API_BASE}/analytics/errors`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};
