// Image Preview Component
// Displays before/after images side by side

import React from 'react';
import '../styles/components.css';

const ImagePreview = ({ hazyImage, dehazedImage, metrics, isLoading }) => {
  const downloadImage = (imageSrc, filename) => {
    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (isLoading) {
    return (
      <div className="preview-container loading">
        <div className="spinner"></div>
        <p>Processing image... (3-5 seconds)</p>
      </div>
    );
  }

  if (!dehazedImage) {
    return null;
  }

  return (
    <div className="preview-container">
      <div className="preview-section">
        <h3>Results</h3>

        <div className="image-comparison">
          <div className="image-box">
            <h4>Before (Hazy)</h4>
            {hazyImage && (
              <img src={hazyImage} alt="Hazy input" className="preview-image" />
            )}
          </div>

          <div className="divider">➜</div>

          <div className="image-box">
            <h4>After (Dehazed)</h4>
            <img
              src={dehazedImage}
              alt="Dehazed output"
              className="preview-image"
            />
          </div>
        </div>

        {/* Metrics Display */}
        {metrics && (
          <div className="metrics-panel">
            <h4>📊 Quality Metrics</h4>

            <div className="metrics-grid">
              {/* PSNR Section */}
              <div className="metric-box">
                <h5>PSNR (dB)</h5>
                {metrics.psnr.hazy_vs_dehazed && (
                  <div className="metric-item">
                    <label>Hazy vs Dehazed:</label>
                    <span className="value">{metrics.psnr.hazy_vs_dehazed}</span>
                  </div>
                )}
                {metrics.psnr.dehazed_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Dehazed vs GT:</label>
                    <span className="value">{metrics.psnr.dehazed_vs_ground_truth}</span>
                  </div>
                )}
                {metrics.psnr.hazy_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Hazy vs GT:</label>
                    <span className="value">{metrics.psnr.hazy_vs_ground_truth}</span>
                  </div>
                )}
              </div>

              {/* SSIM Section */}
              <div className="metric-box">
                <h5>SSIM</h5>
                {metrics.ssim.hazy_vs_dehazed && (
                  <div className="metric-item">
                    <label>Hazy vs Dehazed:</label>
                    <span className="value">{metrics.ssim.hazy_vs_dehazed}</span>
                  </div>
                )}
                {metrics.ssim.dehazed_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Dehazed vs GT:</label>
                    <span className="value">{metrics.ssim.dehazed_vs_ground_truth}</span>
                  </div>
                )}
                {metrics.ssim.hazy_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Hazy vs GT:</label>
                    <span className="value">{metrics.ssim.hazy_vs_ground_truth}</span>
                  </div>
                )}
              </div>

              {/* MSE Section */}
              <div className="metric-box">
                <h5>MSE</h5>
                {metrics.mse.hazy_vs_dehazed && (
                  <div className="metric-item">
                    <label>Hazy vs Dehazed:</label>
                    <span className="value">{metrics.mse.hazy_vs_dehazed}</span>
                  </div>
                )}
                {metrics.mse.dehazed_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Dehazed vs GT:</label>
                    <span className="value">{metrics.mse.dehazed_vs_ground_truth}</span>
                  </div>
                )}
                {metrics.mse.hazy_vs_ground_truth && (
                  <div className="metric-item">
                    <label>Hazy vs GT:</label>
                    <span className="value">{metrics.mse.hazy_vs_ground_truth}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="action-buttons">
          <button
            onClick={() => downloadImage(dehazedImage, 'dehazed_output.jpg')}
            className="action-btn primary"
          >
            ⬇ Download Dehazed Image
          </button>

          {metrics && (
            <button
              onClick={() => {
                const metricsJSON = JSON.stringify(metrics, null, 2);
                const blob = new Blob([metricsJSON], { type: 'application/json' });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'metrics.json';
                link.click();
              }}
              className="action-btn"
            >
              📊 Download Metrics
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImagePreview;
