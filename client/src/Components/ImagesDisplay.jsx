import React from 'react';
import './ImagesDisplay.css'; 

const ImagesDisplay = () => {
  // Assuming Flask backend runs on localhost port 5001
  const beforeProcessingUrl = 'http://localhost:5001/images/before_processing.png';
  const afterProcessingUrl = 'http://localhost:5001/images/after_processing.png';

  return (
    <div className="images-display-container">

        <div className="text-container">
            <h2>EEG Bandpass Frequency Samples</h2>
        </div>

      <div className="image-container">
        <h2>Before Processing</h2>
        <img src={beforeProcessingUrl} alt="Before Processing" />
      </div>

      <div className="image-container">
        <h2>After Processing</h2>
        <img src={afterProcessingUrl} alt="After Processing" />
      </div>

    </div>
  );
};

export default ImagesDisplay;
