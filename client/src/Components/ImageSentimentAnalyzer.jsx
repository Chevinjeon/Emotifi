// Importing necessary hooks and dependencies
import React, { useState } from 'react';

const ImageSentimentAnalyzer = ({ imageUrl }) => {
  const [analysisResult, setAnalysisResult] = useState('');
  const [userInput, setUserInput] = useState('');

  const analyzeSentiment = async () => {
    try {
      // Assuming you have a backend endpoint that calls Google Gemini API
      const response = await fetch('/analyze-sentiment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userInput }),
      });

      if (!response.ok) throw new Error('Network response was not ok.');

      const result = await response.json();
      setAnalysisResult(result.analysis); // Adjust according to the actual response structure
    } catch (error) {
      console.error('Error fetching sentiment analysis:', error);
      setAnalysisResult('Error analyzing sentiment. Please try again.');
    }
  };

  return (
    <div>
      <h3>How does this artwork make you feel?</h3>
      <textarea
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Share your thoughts here..."
        rows="4"
        style={{ width: '100%', marginBottom: '10px' }}
      ></textarea>
      <button onClick={analyzeSentiment}>Analyze Sentiment</button>
      {analysisResult && <p>Sentiment Analysis: {analysisResult}</p>}
    </div>
  );
};

export default ImageSentimentAnalyzer;
