import React, { useState } from 'react';

const ImageSentimentAnalyzer = () => {
  const [analysisResult, setAnalysisResult] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Function to handle image upload
  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedImage(e.target.files[0]);
    }
  };

  // Function to upload the image to the Flask backend and get the analysis
  const analyzeImageSentiment = async () => {
    if (!selectedImage) {
      alert('Please select an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5001/analyze-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setAnalysisResult(data); //  might need to adjust this depending on the structure of response
    } catch (error) {
      console.error('Error during image analysis:', error);
      setAnalysisResult('Error analyzing the image.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h3>Analyze your generated artwork</h3>
      <input type="file" onChange={handleImageChange} accept="image/*" />
      <button onClick={analyzeImageSentiment} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Analyze Image'}
      </button>
      {analysisResult && <div><p>Analysis Result:</p><p>{JSON.stringify(analysisResult)}</p></div>}
    </div>
  );
};

export default ImageSentimentAnalyzer;
