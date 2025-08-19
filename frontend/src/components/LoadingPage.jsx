import React from 'react';
import './LoadingPage.css';

const LoadingPage = () => {
  return (
    <section className="loading-page">
      <div className="loading-text">
        <h1>Create a WordPress plugin without writing code</h1>
        <p>Quick explanation of how the tool works.</p>
        <button className="cta-button">Start creating your plugin</button>
      </div>
      <div className="loading-illustration">
        <img
            src="https://bing.com/th/id/BCO.61acdfeb-79c6-44d0-bde8-9324bb6cfa6d.png"
            alt="AI chatbot with headset and WordPress logo"
            className="illustration-image"
        />
      </div>
    </section>
  );
};

export default LoadingPage;