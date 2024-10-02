import React from 'react';
import Navbar from './Navbar';

const DashboardLayout = ({ children, handleLogout }) => {
  return (
    <div className="dashboard-layout">
      <Navbar handleLogout={handleLogout} />  {/* Pass handleLogout */}
      <div className="dashboard-content">
        {children}
      </div>
    </div>
  );
};

export default DashboardLayout;
