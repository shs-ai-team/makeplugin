import React, { useState, useEffect, useRef } from 'react';
import './PluginGeneratorPage.css';

const PluginGeneratorPage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [prompts, setPrompts] = useState([]);

  const promptListRef = useRef(null);

  // 👇 Initial bot message on first load
  useEffect(() => {
    setPrompts([
      {
        type: 'bot',
        content: `I’ll create a comprehensive contact form plugin for you. This will include:
- Customizable fields
- Email notifications to admin
- reCAPTCHA spam protection
- Form submission storage
- Responsive design`
      }
    ]);
  }, []);

  // 👇 Handle screen resize
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
      setIsSidebarOpen(window.innerWidth > 768);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // 👇 Scroll to bottom when prompts update
  useEffect(() => {
    if (promptListRef.current) {
      promptListRef.current.scrollTop = promptListRef.current.scrollHeight;
    }
  }, [prompts]);

  // 👇 Handle user input
  const handleGenerate = () => {
    if (inputValue.trim() === '') return;
    setPrompts(prev => [
      ...prev,
      { type: 'user', content: inputValue.trim() }
    ]);
    setInputValue('');
  };


  const handleResetChat = () => {
    setPrompts([]);
    setInputValue('');
    if (isMobile) {
      setIsSidebarOpen(false);
    }
  };

  return (
    <div className="layout">
      {/* Sidebar */}
      {isSidebarOpen && (
        <aside className={`sidebar ${isSidebarOpen && isMobile ? 'mobile-visible' : ''}`}>
          <div className="sidebar-top">
            <h2 className="logo">MakePlugin</h2>
            <button className="new-chat" onClick={handleResetChat}>New Chat</button>
          </div>
          <div className="recent-chats">
            <h3>Recent Chats</h3>
            <ul>
              <li><span className="chat-icon">💬</span> Contact Form Plugin <span className="time">2h ago</span></li>
              <li><span className="chat-icon">📅</span> Event Calendar <span className="time">1d ago</span></li>
              <li><span className="chat-icon">📄</span> Custom Post Types <span className="time">3d ago</span></li>
            </ul>
          </div>
        </aside>
      )}

      {/* Main Content */}
      <main className={`main ${isSidebarOpen && isMobile ? 'hide-on-mobile' : ''}`}>
        <div className="plugin-header-box">
          <div className="header">
            <h1>Plugin Generator</h1>
            <span className="plugin-count">23 plugins remaining this month</span>
            {isMobile && (
              <button className="toggle-sidebar" onClick={() => setIsSidebarOpen(prev => !prev)}>☰</button>
            )}
          </div>
          <p className="subtitle">Describe your plugin and I'll build it for you</p>
        </div>

        <div ref={promptListRef} className="chat-container">
          {prompts.map((msg, index) => (
            <div key={index} className={msg.type === 'bot' ? 'response-box' : 'example-prompt'}>
              {msg.content}
            </div>
          ))}
        </div>
        <div className="input-wrapper">
          <div className="input-row">
            <textarea
              className="plugin-input"
              placeholder="Describe the WordPress plugin you want to create..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            ></textarea>
            <button className="generate-button" onClick={handleGenerate}>➣</button>
          </div>

          <p className="hint">
            Be specific about features, functionality, and design preferences for best results.
          </p>
        </div>
      </main>
    </div>
  );
};

export default PluginGeneratorPage;
