import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PdfViewer = ({ pdfPath }) => {
  const [pdfUrl, setPdfUrl] = useState('');

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        // Extract the filename from pdfPath
        const pdfFilename = pdfPath.split('/').pop(); // Get just the filename
        
        const response = await axios.get(`http://localhost:5000/download/${pdfFilename}`, {
          responseType: 'blob',
        });

        const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
        const pdfUrl = URL.createObjectURL(pdfBlob);

        setPdfUrl(pdfUrl);
      } catch (error) {
        console.error('Error fetching PDF:', error);
      }
    };

    fetchPdf();
  }, [pdfPath]);

  return (
    <div>
      <h2>PDF Viewer</h2>
      {pdfUrl ? (
        <iframe src={pdfUrl} width="100%" height="600px" />
      ) : (
        <p>Loading PDF...</p>
      )}
    </div>
  );
};

export default PdfViewer;
