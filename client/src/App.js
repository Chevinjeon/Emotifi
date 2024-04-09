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
  const handleAudioPlay = () => {
    let audioContext = new AudioContext();
    if (!source.current) {
      source.current = audioContext.createMediaElementSource(audioRef.current);
      analyzer.current = audioContext.createAnalyser();
      source.current.connect(analyzer.current);
      analyzer.current.connect(audioContext.destination);
    }
    visualizeData();
  };

  // Visualization logic
  const visualizeData = () => {
    animationController = window.requestAnimationFrame(visualizeData);
  if (audioRef.current.paused) {
    return cancelAnimationFrame(animationController);
  }
  const songData = new Uint8Array(140);
  analyzer.current.getByteFrequencyData(songData);
  const bar_width = 3;
  let start = 0;
  const ctx = canvasRef.current.getContext("2d");
  ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  for (let i = 0; i < songData.length; i++) {
    // compute x coordinate where we would draw
    start = i * 4;
    //create a gradient for the  whole canvas
    let gradient = ctx.createLinearGradient(
      0,
      0,
      canvasRef.current.width,
      canvasRef.current.height
    );
    gradient.addColorStop(0.2, "#2392f5");
    gradient.addColorStop(0.5, "#fe0095");
    gradient.addColorStop(1.0, "purple");
    ctx.fillStyle = gradient;
    ctx.fillRect(start, canvasRef.current.height, bar_width, -songData[i]);
  }
  }; 


  const handleGenerate = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 2599); 
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

  /*
  // Scroll event listener to play audio at bottom of the page 
  useEffect(() => { 
    const handleScroll = () => { 
      const bottom = Math.ceil(window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight;
      if (bottom && file) {
        audioRef.current.play(); 
      } 
    };
    window.addEventListener('scroll', handleScroll);

    return () => window.removeEventListener('scroll', handleScroll);
  }, [file]); // Depend on file to ensure this effect runs when the file changes 

*/

/*connect React application with backend route for create_audio.py*/
const handleGenerateMidi = async () => {
  /*const notes =  convert data to the required format*/;
  const response = await fetch('http://localhost:5000/generate-midi', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({notes}),
  });

  if (response.ok) { 
    const blob = await response.blob();
    const url = URL.createObjectUTL(blob);
    setFile(url); //assuming setFile will then set the audio source 
  } else {
    console.error('Failed to generate MIDI');
  }
};

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