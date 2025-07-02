import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <div className="header-container">
      {/* Animated Background Elements */}
      <div className="header-floating-shapes">
        <div className="header-floating-shape"></div>
        <div className="header-floating-shape"></div>
        <div className="header-floating-shape"></div>
      </div>

      <header className="header">
        <div className="header-content">
          <h1 className="header-title">📈 SmartStocks AI</h1>
          <p className="header-tagline">Your intelligent stock analysis companion</p>
          
          {/* Optional: Navigation or action buttons */}
          <div className="header-actions">
            <div className="status-indicator">
              <div className="status-dot"></div>
              <span>Live Market Data</span>
            </div>
          </div>
        </div>
      </header>
    </div>
  );
};

export default Header;