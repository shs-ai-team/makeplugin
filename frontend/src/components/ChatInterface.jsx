import React, { useState } from 'react';
import './ChatInterface.css'; // We'll create this for styling
import { generatePlugin } from '../api';

const ChatInterface = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    setDownloadUrl(null);

    try {
      const blob = await generatePlugin(prompt);
      
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>Describe Your Plugin</h1>
      <p>Tell our AI what your WordPress plugin should do, and we'll generate it for you.</p>
      
      <form onSubmit={handleSubmit}>
        <textarea
          className="prompt-input"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., Create a plugin that adds a shortcode [current_year]..."
          rows="4"
          disabled={isLoading}
        />
        <button type="submit" className="generate-button" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Plugin'}
        </button>
      </form>

      {error && <div className="error-message">Error: {error}</div>}
      
      {downloadUrl && (
        <div className="download-section">
          <h2>✅ Success!</h2>
          <p>Your plugin is ready for download.</p>
          <a href={downloadUrl} download="generated-plugin.zip" className="download-button">
            Download Plugin (.zip)
          </a>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;