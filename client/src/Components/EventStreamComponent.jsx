import React, { useState, useEffect } from 'react';

const EventStreamComponent = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:5001/stream");

    eventSource.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div>
      <h2>Live Updates</h2>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default EventStreamComponent;
