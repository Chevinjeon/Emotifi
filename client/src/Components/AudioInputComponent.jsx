import React, { useState, useContext } from 'react';
import { MoodContext } from '../Context/MoodContext'

const AudioInputComponent = () => {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const { setMood } = useContext(MoodContext);

  const handleStartRecording = () => {
    // Start recording
  };

  const handleStopRecording = () => {
    // Stop recording and setAudioBlob
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    const response = await fetch('http://localhost:5000/upload-audio', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    setMood(data.mood); // Assuming mood is returned
    // Trigger downstream actions like art and music generation
  };

  return (
    <div>
      {recording ? (
        <button onClick={handleStopRecording}>Stop Recording</button>
      ) : (
        <button onClick={handleStartRecording}>Start Recording</button>
      )}
      <button onClick={handleUpload} disabled={!audioBlob}>Upload and Analyze</button>
    </div>
  );
};

export default AudioInputComponent;
