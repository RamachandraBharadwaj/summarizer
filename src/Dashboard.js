// In your Dashboard.js

import React, { useState } from 'react';
import axios from 'axios';
import PdfViewer from './PdfViewer'; // Import PdfViewer

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [pdfPath, setPdfPath] = useState(''); // State to hold the PDF path

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        alert('File uploaded successfully');
        setPdfPath(response.data.pdf_path); // Store the returned PDF path
      } catch (error) {
        console.error('File upload failed:', error);
        alert('File upload failed');
      }
    }
  };

  return (
    <div className="dashboard-content">
      <h1>Upload your ZAP report</h1>
      {/* File picker */}
      <input type="file" className="file-picker" onChange={handleFileChange} />
      {/* Upload button */}
      <button onClick={handleFileUpload}>Upload</button>
      {/* Render PdfViewer if pdfPath is set */}
      {pdfPath && <PdfViewer pdfPath={pdfPath} />}
    </div>
  );
};

export default Dashboard;
