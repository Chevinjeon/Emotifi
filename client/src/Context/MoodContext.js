import { createContext, useContext, useState } from 'react';

const MoodContext = createContext(null);

export const useMood = () => useContext(MoodContext);

export const MoodProvider = ({ children }) => {
  const [mood, setMood] = useState('');

  return (
    <MoodContext.Provider value={{ mood, setMood }}>
      {children}
    </MoodContext.Provider>
  );
};
