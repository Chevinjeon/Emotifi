import React, { useState, useRef } from 'react';
import './App.css';
import VideoComponent from './Components/VideoComponent'; // Adjust the path as per your project structure
import ImageGenerator from './Assets/ImageGenerator/ImageGenerator';
import Animation from './Assets/Animation.mp4';
import { FaArrowDown } from 'react-icons/fa'; 
import { useEffect } from 'react';

let animationController;

function App() {

  // Existing state and refs (video constants)
  const [isLoading, setIsLoading] = useState(false);
  const [showArrow, setShowArrow] = useState(false);
  const [showImage, setShowImage] = useState(false); // Add this state variable

  //webaudio constants
  const [file, setFile] = useState(null);
  const canvasRef = useRef();
  const audioRef = useRef(); 
  const source = useRef(); 
  const analyzer = useRef();

   // Logic to handle audio play
  const handleAudioPlay = () => {};

  // Visualization logic
  const visualizeData = () => {}; 


  const handleGenerate = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 3000); 
  };

  useEffect(() => {
    // Show the arrow after 1 second
    const timer1 = setTimeout(() => {
      setShowArrow(true);
    }, 1000);

    // Hide the arrow after an additional 2 seconds
    const timer2 = setTimeout(() => {
      setShowArrow(false);
    }, 8000);

    // Clear timeouts when component unmounts
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);


  return (
    <div className="App">
      <div className="video-container">
        <header className="video-overlay-header">
          <h1>See what your EEG (electroencephalogram) brain signals can generate!</h1>
        </header>
        <VideoComponent src="./Animation.mp4" />
      </div>
      <ImageGenerator isLoading={isLoading} />
      {showArrow && (
        <div className="scroll-down">
          <FaArrowDown />
          <p>Scroll Down</p>
        </div>
      )}
      {/* New elements for file upload, audio play, and canvas */}
      <input
        type="file"
        onChange={({ target: { files } }) => files[0] && setFile(files[0])}
      />
      {file && (
        <audio
          ref={audioRef}
          onPlay={handleAudioPlay}
          src={window.URL.createObjectURL(file)}
          controls
        />
      )}
      <canvas ref={canvasRef} width={500} height={200} />

    </div>
  );
}

export default App;