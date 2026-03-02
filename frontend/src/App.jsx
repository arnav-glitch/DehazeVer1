// Main App Component
// Orchestrates the entire dehazing workflow

import React, { useState, useEffect } from 'react';
import './styles/main.css';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import DehazeAPI from './services/api';

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [apiReady, setApiReady] = useState(false);
  const [hazyImageSrc, setHazyImageSrc] = useState(null);
  const [dehazedImageSrc, setDehazedImageSrc] = useState(null);
  const [metrics, setMetrics] = useState(null);

  // Check API health on mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await DehazeAPI.health();
        setApiReady(true);
        console.log('✓ API is ready');
      } catch (err) {
        setError('API server not available. Please ensure backend is running on port 5000.');
        console.error('API health check failed:', err);
      }
    };

    checkAPI();
  }, []);

  const handleImagesSelected = async (hazyFile, groundTruthFile) => {
    setIsProcessing(true);
    setError(null);
    setMetrics(null);

    try {
      // Display hazy image
      const hazyReader = new FileReader();
      hazyReader.onload = (e) => {
        setHazyImageSrc(e.target.result);
      };
      hazyReader.readAsDataURL(hazyFile);

      // Process with or without metrics
      let response;
      if (groundTruthFile) {
        response = await DehazeAPI.dehazeImageWithMetrics(hazyFile, groundTruthFile);
      } else {
        response = await DehazeAPI.dehazeImage(hazyFile);
      }

      if (response.success) {
        setDehazedImageSrc(response.dehazed_image);
        if (response.metrics) {
          setMetrics(response.metrics);
        }
        console.log(
          `✓ Processing completed in ${response.processing_time_ms}ms`
        );
      } else {
        setError('Processing failed');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'An error occurred during processing');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNewImage = () => {
    setHazyImageSrc(null);
    setDehazedImageSrc(null);
    setMetrics(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🌫️ Image Dehazing Application</h1>
          <p>Remove haze from images using AI</p>
          {apiReady ? (
            <span className="status-badge ready">✓ API Ready</span>
          ) : (
            <span className="status-badge error">✗ API Offline</span>
          )}
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span>⚠ {error}</span>
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {!dehazedImageSrc ? (
          <ImageUpload
            onImagesSelected={handleImagesSelected}
            isProcessing={isProcessing}
          />
        ) : (
          <ImagePreview
            hazyImage={hazyImageSrc}
            dehazedImage={dehazedImageSrc}
            metrics={metrics}
            isLoading={isProcessing}
          />
        )}

        {dehazedImageSrc && (
          <div className="new-image-button-container">
            <button
              onClick={handleNewImage}
              className="new-image-btn"
            >
              ⟲ Process Another Image
            </button>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Dehaze v1.0 | Using MAXIM-S2 model with Trainable Adapter |{' '}
          <a href="https://github.com" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
