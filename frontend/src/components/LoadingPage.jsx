import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LoadingPage.css';

const LoadingPage = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate('/plugin-generator');
  };

  return (
    <section className="loading-page">
      <div className="loading-text">
        <h1>Create a WordPress plugin without writing code</h1>
        <p>Your friendly WordPress Plugin Assistant. Describe your desired function and receive a finished plugin as a ZIP file for download.</p>
        <button className="cta-button" onClick={handleStart}>
          Start creating your plugin
        </button>
      </div>
      <div className="loading-illustration">
        <img
          src="./makeplugin_logo.png"
          alt="AI chatbot with headset and WordPress logo"
          className="illustration-image"
        />
      </div>
    </section>
  );
};

export default LoadingPage;
