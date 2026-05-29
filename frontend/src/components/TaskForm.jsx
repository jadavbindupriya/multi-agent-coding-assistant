import React, { useState } from 'react';

function TaskForm({ onSubmit, loading }) {
  const [task, setTask] = useState('');
  const [language, setLanguage] = useState('python');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (task.trim()) {
      onSubmit(task, language);
      setTask('');
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="task">Coding Task:</label>
        <textarea
          id="task"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="e.g., Write a function to check if a number is prime"
          disabled={loading}
          rows="4"
        />
      </div>

      <div className="form-group">
        <label htmlFor="language">Language:</label>
        <select
          id="language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          disabled={loading}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      <button
        type="submit"
        className="submit-btn"
        disabled={loading || !task.trim()}
      >
        {loading ? 'Processing...' : '🚀 Submit Task'}
      </button>
    </form>
  );
}

export default TaskForm;