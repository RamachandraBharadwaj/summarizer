import React from 'react';

const Dashboard = () => {
  return (
    <div className="dashboard-content">
      <h1>Upload your ZAP report</h1>
      {/* File picker component */}
      <input type="file" className="file-picker" />
      {/* Additional dashboard content can go here */}
    </div>
  );
};

export default Dashboard;
