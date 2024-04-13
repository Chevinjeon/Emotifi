import React, { useEffect, useState } from 'react';

const ImageSentimentAnalyzer = () => {
  const [analysisResult, setAnalysisResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchAnalysisResult = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:5001/get-analysis');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setAnalysisResult(data); // Adjust based on the response structure
      } catch (error) {
        console.error('Error fetching analysis:', error);
        setAnalysisResult('Error fetching analysis.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalysisResult();
  }, []);

  return (
    <div>
      <h3>Analysis of Generated Artwork</h3>
      {isLoading ? (
        <p>Loading analysis...</p>
      ) : (
        <div>
          <p>Analysis Result:</p>
          <p>{JSON.stringify(analysisResult)}</p>
        </div>
      )}
    </div>
  );
};

export default ImageSentimentAnalyzer;
