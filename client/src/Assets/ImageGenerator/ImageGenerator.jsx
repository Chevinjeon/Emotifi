import React, { useState } from 'react';
import axios from 'axios'; // Make sure axios is installed
import './ImageGenerator.css'; // Assuming you have CSS for this component

const ImageGenerator = ({ mood }) => {
  const [imageUrl, setImageUrl] = useState('');
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchGeneratedImage = (mood, style) => {
    setLoading(true);
    setError('');

    // Construct the API URL and body data
    const apiUrl = 'http://localhost:5001/get-art';
    const postData = {
      mood: mood,
      style: style
    };

    axios.post(apiUrl, postData, {
        headers: {
            'Content-Type': 'application/json'
        },
        responseType: 'blob'
    })
      .then(response => {
        const blob = new Blob([response.data], { type: 'image/png' });
        const url = URL.createObjectURL(blob);
        setImageUrl(url);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load generated image');
        setLoading(false);
        console.error('Error fetching the generated image:', err);
      });
  };

  return (
    <div className='ai-image-generator'>
      <div className="header">Emotion AI <span>Visualization</span></div>
      {isLoading ? (
        <p>Loading...</p>
      ) : imageUrl ? (
        <div className="image">
          <img src={imageUrl} alt="Generated Art" onError={() => setError('Failed to load image')} />
        </div>
      ) : (
        error && <p>Error: {error}</p>
      )}
      <p>This artwork is generated from your mood analyzed from your brainwave signals:</p>
      <div className="generate-btn" onClick={() => fetchGeneratedImage('happy', 'abstract')}>
        Request Image
      </div>
      <iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1EIgG2NEOhqsD7?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </div>
  );
};

export default ImageGenerator;
