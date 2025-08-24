import logoImg from '../assets/makeplugin_logo2.png';

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LoadingPage.css';

const LoadingPage = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate('/plugin-generator');
  };

  return (
    <div className="loading-page">
      <div className="hero">
        <div className="hero-illustration">
          <img
            src={logoImg}
            alt="AI chatbot with WordPress"
          />
        </div>
        <div className="hero-text">
          {/* <h1>Make Plugin</h1> */}
          <h2> Generate WordPress Plugins in Minutes </h2>
          <p>Describe your idea and watch AI build it—no coding required.</p>
          <button className="cta-button" onClick={handleStart}>
            Make A Plugin Now
          </button>
        </div>
        
      </div>

      <div className="flow">
        <div className="step">
          <div className="icon">💬</div>
          <h3>Describe</h3>
          {/* <p>Tell Make Plugin what plugin you want.</p> */}
        </div>
        <div className="step">
          <div className="icon">🧠</div>
          <h3>Refine</h3>
          {/* <p>AI optimizes your concept into code.</p> */}
        </div>
        <div className="step">
          <div className="icon">📦</div>
          <h3>Develop</h3>
          {/* <p>Get your ready-to-use WordPress plugin instantly.</p> */}
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;


// import React from 'react';
// import { useNavigate } from 'react-router-dom';
// import './LoadingPage.css';

// const LoadingPage = () => {
//   const navigate = useNavigate();

//   const handleStart = () => {
//     navigate('/plugin-generator');
//   };

//   return (
//     <section className="loading-page">
//       <div className="loading-text">
//         <h1>Create a WordPress plugin without writing code</h1>
//         <p>Quick explanation of how the tool works.</p>
//         <button className="cta-button" onClick={handleStart}>
//           Start creating your plugin
//         </button>
//       </div>
//       <div className="loading-illustration">
//         <img
//           src="https://bing.com/th/id/BCO.61acdfeb-79c6-44d0-bde8-9324bb6cfa6d.png"
//           alt="AI chatbot with headset and WordPress logo"
//           className="illustration-image"
//         />
//       </div>
//     </section>
//   );
// };

// export default LoadingPage;


