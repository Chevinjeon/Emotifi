// ReadingComponent.jsx
import React from 'react';
import './ReadingComponent.css';
import reading from '../Assets/reading.mp4'; // Your video path

const ReadingComponent = ({ isLoading, stopVideo }) => {
  return (
    <div className="video-container">
      {isLoading && (
        <div className="loading-overlay">
          Loading...
        </div>
      )}
      <video width="1920" height="1080" autoPlay muted loop>
        <source src={reading} type="video/mp4" />
      </video>
    </div>
  );
};

export default ReadingComponent;
