// Image Upload Component with Drag-Drop
// Allows users to upload hazy images with optional ground truth

import React, { useState } from 'react';
import '../styles/components.css';

const ImageUpload = ({ onImagesSelected, isProcessing }) => {
  const [dragActive, setDragActive] = useState(false);
  const [hazyFile, setHazyFile] = useState(null);
  const [groundTruthFile, setGroundTruthFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isProcessing) {
      setDragActive(e.type === 'dragenter' || e.type === 'dragover');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (isProcessing) return;

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        setHazyFile(file);
      } else {
        alert('Please drop an image file');
      }
    }
  };

  const handleFileSelect = (e, isGroundTruth = false) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        if (isGroundTruth) {
          setGroundTruthFile(file);
        } else {
          setHazyFile(file);
        }
      } else {
        alert('Please select an image file');
      }
    }
  };

  const handleSubmit = () => {
    if (hazyFile) {
      onImagesSelected(hazyFile, groundTruthFile);
    } else {
      alert('Please select a hazy image first');
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-section">
        <h2>Image Dehazing Service</h2>

        {/* Hazy Image Upload */}
        <div
          className={`drag-drop-area ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="hazy-file"
            accept="image/*"
            onChange={(e) => handleFileSelect(e, false)}
            disabled={isProcessing}
            style={{ display: 'none' }}
          />
          <label htmlFor="hazy-file" className="drag-drop-label">
            <div className="icon">📁</div>
            <h3>Drop Hazy Image Here</h3>
            <p>or click to select</p>
            <small>(JPG, PNG, BMP, WEBP, TIFF)</small>
          </label>
        </div>

        {hazyFile && (
          <div className="file-info">
            <span className="file-name">{hazyFile.name}</span>
            <button
              onClick={() => setHazyFile(null)}
              disabled={isProcessing}
              className="remove-btn"
            >
              ✕
            </button>
          </div>
        )}

        {/* Ground Truth Image Upload (Optional) */}
        <div className="optional-section">
          <h3>Ground Truth (Optional)</h3>
          <p>Upload the clean/dehazed image to calculate metrics (PSNR, SSIM)</p>

          <div className="ground-truth-upload">
            <input
              type="file"
              id="gt-file"
              accept="image/*"
              onChange={(e) => handleFileSelect(e, true)}
              disabled={isProcessing}
              style={{ display: 'none' }}
            />
            <label htmlFor="gt-file" className="file-select-label">
              {groundTruthFile ? (
                <span>{groundTruthFile.name} ✓</span>
              ) : (
                <span>Choose Ground Truth Image</span>
              )}
            </label>

            {groundTruthFile && (
              <button
                onClick={() => setGroundTruthFile(null)}
                disabled={isProcessing}
                className="remove-btn-small"
              >
                Remove
              </button>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={!hazyFile || isProcessing}
          className="submit-btn"
        >
          {isProcessing ? 'Processing...' : 'Process Image'}
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;
