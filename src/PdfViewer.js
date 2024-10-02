import React from 'react';

const PdfViewer = ({ pdfPath }) => {
  return (
    <div>
      <h2>PDF Viewer</h2>
      {pdfPath ? (
        <iframe src={`http://localhost:5000/download/${pdfPath.split('/').pop()}`} width="100%" height="600px" />
      ) : (
        <p>Loading PDF...</p>
      )}
    </div>
  );
};

export default PdfViewer;
