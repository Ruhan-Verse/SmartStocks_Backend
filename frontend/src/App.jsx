import React from 'react';
import Header from './components/Header';
import ChatBox from './components/Chatbox';

const App = () => {
  return (
    <div className="app-container">
      <Header />
      <div className="main-content">
        <ChatBox />
      </div>
    </div>
  );
};

export default App;
