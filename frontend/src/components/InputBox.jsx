import React, { useState } from 'react';

function InputBox({ onSubmit, loading, language, setLanguage }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input, language);
      setInput('');
    }
  };

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <div className="input-controls">
        <select 
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          disabled={loading}
          className="language-select"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      <div className="input-wrapper">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your coding task..."
          disabled={loading}
          className="input-field"
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()}
          className="send-button"
        >
          {loading ? '⏳' : '➤'}
        </button>
      </div>
    </form>
  );
}

export default InputBox;
