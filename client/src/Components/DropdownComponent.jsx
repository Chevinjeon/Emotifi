import React, { useState } from 'react';
import ReadingComponent from './ReadingComponent';
import './DropdownComponent.css';
import startbutton from '../Assets/startbutton.png'; // Adjust the path as needed

const DropDownComponent = () => {
  const [selection, setSelection] = useState('');
  const [showReading, setShowReading] = useState(false);

  const handleSelectionChange = (event) => {
    setSelection(event.target.value);
  };

  const handleStartClick = async () => {
    if (!selection) {
        alert('Please make a selection first.');
        return;
    }

    try {
        const response = await fetch('http://your-flask-server:5001/handle-selection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ option: selection })
        });
        if (response.ok) {
            const data = await response.json();
            console.log("Success:", data);
            // Handle the response data here
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

  return (
    <div>
      <select onChange={handleSelectionChange} value={selection}>
        <option value="">Select an option</option>
        <option value="sample">Use a sample brainwave recording</option>
        <option value="own">Use your own brainwaves - requires headset configuration</option>
      </select>
      <div onClick={handleStartClick} style={{ cursor: 'pointer' }}>
        <img src={startbutton} alt="Start" className="startbutton" />
      </div>
      {showReading && <ReadingComponent />}
    </div>
  );
};

export default DropDownComponent;
