import React from 'react';

const Navbar = ({ handleLogout }) => {
  return (
    <nav className="navbar">
      <a href="/dashboard">Home</a>
      {/* Logout link that calls handleLogout */}
      <a href="#" onClick={(e) => { e.preventDefault(); handleLogout(); }} className="logout-link">
        Logout
      </a>
    </nav>
  );
};

export default Navbar;
