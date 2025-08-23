import React, { useState, useEffect, useRef } from 'react';
import './PluginGeneratorPage.css';
// 👇 1. Import all our API service functions
import * as api from '../apiService';

const PluginGeneratorPage = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [isMobile, setIsMobile] = useState(false);
    const [inputValue, setInputValue] = useState('');

    // 👇 2. Add new state to manage the chat session and UI
    const [sessionId, setSessionId] = useState(null);
    const [messages, setMessages] = useState([]); // Renamed from 'prompts'
    const [isLoading, setIsLoading] = useState(true); // Start loading initially
    const [isInputDisabled, setIsInputDisabled] = useState(false);

    const chatContainerRef = useRef(null);

    // 👇 3. Function to start a new chat session
    const startNewChat = async () => {
        setIsLoading(true);
        setIsInputDisabled(false);
        setInputValue('');
        try {
            const data = await api.startNewSession();
            setSessionId(data.session_id);
            setMessages(data.messages);
        } catch (error) {
            console.error("Failed to start new session:", error);
            // Optionally, set an error message to display in the UI
            setMessages([{ role: 'consultant', content: 'Sorry, I couldn\'t connect to the server. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    // 👇 4. useEffect to start the session on first load
    useEffect(() => {
        startNewChat();
    }, []);

    // Handle screen resize (no changes needed here)
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth <= 768);
            setIsSidebarOpen(window.innerWidth > 768);
        };
        handleResize();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // Scroll to bottom when messages update (no changes needed here)
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);
    
    // 👇 5. useEffect to handle polling for the developer response
    useEffect(() => {
        if (isInputDisabled) {
            const intervalId = setInterval(async () => {
                try {
                    const response = await api.getDeveloperResponse(sessionId);
                    if (response.success) {
                        clearInterval(intervalId); // Stop polling
                        setMessages(prev => [...prev, response.message]);
                        setIsLoading(false);
                    }
                } catch (error) {
                    console.error("Polling failed:", error);
                    clearInterval(intervalId); // Stop polling on error
                    setIsLoading(false);
                }
            }, 5000); // Poll every 5 seconds

            return () => clearInterval(intervalId); // Cleanup on component unmount
        }
    }, [isInputDisabled, sessionId]);


    // 👇 6. Updated handler to send user message to the API
    const handleSendMessage = async () => {
        if (inputValue.trim() === '' || !sessionId) return;

        const userMessage = { role: 'user', content: inputValue.trim() };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await api.sendUserMessage(sessionId, userMessage.content);
            setMessages(prev => [...prev, response.message]);

            if (response.message.requirements_finalized) {
                setIsInputDisabled(true);
                // The polling useEffect will now take over
            } else {
                setIsLoading(false);
            }
        } catch (error) {
            console.error("Failed to send message:", error);
            setIsLoading(false);
        }
    };

    const handleResetChat = () => {
        startNewChat(); // Simply start a new session
        if (isMobile) {
            setIsSidebarOpen(false);
        }
    };
    
    // Helper to render message content, especially for developer messages
    const renderMessageContent = (msg) => {
        if (msg.role === 'developer' && msg.zip_id) {
            const downloadUrl = api.getPluginDownloadUrl(sessionId, msg.zip_id);
            return (
                <>
                    {msg.content}
                    <a href={downloadUrl} className="download-button" download>
                        Download Plugin (.zip)
                    </a>
                </>
            );
        }
        return msg.content;
    };

    return (
        <div className="layout">
            {/* Sidebar (no changes) */}
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

                {/* 👇 7. Updated chat container to use 'messages' state */}
                <div ref={chatContainerRef} className="chat-container">
                    {messages.map((msg, index) => (
                        <div key={index} className={msg.role === 'user' ? 'example-prompt' : 'response-box'}>
                            {renderMessageContent(msg)}
                        </div>
                    ))}
                    {isLoading && <div className="response-box"><span></span></div>}
                </div>

                <div className="input-wrapper">
                    <div className="input-row">
                        <textarea
                            className="plugin-input"
                            placeholder="Describe the WordPress plugin you want to create..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            // 👇 8. Disable input when needed
                            disabled={isInputDisabled || isLoading}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSendMessage();
                                }
                            }}
                        />
                        <button
                            className="generate-button"
                            onClick={handleSendMessage}
                            disabled={isInputDisabled || isLoading}
                        >
                            ➣
                        </button>
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