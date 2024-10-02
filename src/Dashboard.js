import React, { useState } from 'react';
import axios from 'axios';
import PdfViewer from './PdfViewer';  // Import the PdfViewer component

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [pdfPath, setPdfPath] = useState('');

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
        const pdfPath = response.data.pdf_path;  // Get the PDF path from the response
        setPdfPath(pdfPath);  // Save PDF path to state
        alert('File uploaded successfully');
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

      {/* Display PDF viewer once PDF is available */}
      {pdfPath && <PdfViewer pdfPath={pdfPath} />}
    </div>
  );
};

export default Dashboard;
