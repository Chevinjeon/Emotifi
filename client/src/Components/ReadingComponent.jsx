import React, { useState, useEffect } from 'react';
import './VideoComponent.css'; // Import the CSS file for styling
import reading from '../Assets/reading.mp4';

const ReadingComponent = () => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // set a timeout to change the state AFTER 3 SECONDS 
    const timer = setTimeout(() => setIsVisible(false), 6000);

    return () => clearTimeout(timer); 
  }, []);

  return (
    <div className={isVisible ? 'video-container' : 'video-container fade-out'}>
      <video width="1920" height="1080" autoPlay muted loop>
      <source src={reading} type="video/mp4" />
      </video>
    </div>
  );
};

export default ReadingComponent;
