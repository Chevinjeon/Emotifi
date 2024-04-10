import React, { useState, useEffect } from 'react';
import './VideoComponent.css'; // Import the CSS file for styling
import reading from '../Assets/reading.gif';

const ReadingComponent = () => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // set a timeout to change the state AFTER 3 SECONDS 
    const timer = setTimeout(() => setIsVisible(false), 6000);

    return () => clearTimeout(timer); 
  }, []);

  return (
    <div className={isVisible ? 'video-container' : 'video-container fade-out'}>
      <img src={reading} alt="Reading" width="1920" height="1080" />
    </div>
  );
};

export default ReadingComponent;
