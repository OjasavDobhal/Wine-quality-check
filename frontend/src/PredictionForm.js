import React, { useState } from 'react';
import axios from 'axios';
import './PredictionForm.css';


function PredictionForm() {
  const [formData, setFormData] = useState({
    fixed_acidity: '',
    volatile_acidity: '',
    citric_acid: '',
    residual_sugar: '',
    chlorides: '',
    free_sulfur_dioxide: '',
    total_sulfur_dioxide: '',
    density: '',
    pH: '',
    sulphates: '',
    alcohol: ''
  });

  const [result, setResult] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError('');
    setResult('');

    try {
      const form = new FormData();
      form.append('file', file);

      const res = await axios.post('http://127.0.0.1:8000/extract', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (res.data.status === "success") {
        const cleaned = {};
        for (const [key, value] of Object.entries(res.data.extracted)) {
          cleaned[key] = value || '';
        }
        setFormData(cleaned);
        setResult('Data extracted successfully!');
      } else {
        throw new Error(res.data.error || 'Extraction failed');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult('');

    // Convert all values to numbers
    const numericData = {};
    for (const [key, value] of Object.entries(formData)) {
      numericData[key] = parseFloat(value) || 0;
    }

    try {
      const res = await axios.post('http://127.0.0.1:8000/predict', numericData, {
        headers: { 'Content-Type': 'application/json' }
      });

      if (res.data.status === "success") {
        setResult(`Predicted Quality: ${res.data.quality} (Class ${res.data.prediction})`);
      } else {
        throw new Error(res.data.message || 'Prediction failed');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  return (
    <div className="form-container">
      <h2>🍷 Wine Quality Predictor</h2>
      
      {error && <div className="error-message">{error}</div>}
      {result && <div className="success-message">{result}</div>}

      <div className="file-upload-section">
        <input 
          type="file" 
          accept="application/pdf" 
          onChange={(e) => setFile(e.target.files[0])} 
          disabled={loading}
        />
        <button 
          onClick={handleFileUpload} 
          disabled={loading || !file}
          className={loading ? 'loading' : ''}
        >
          {loading ? "Extracting..." : "Extract from Report"}
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, val]) => (
          <div key={key} className="input-group">
            <label>{key.replace(/_/g, ' ')}:</label>
            <input
              type="number"
              step="any"
              name={key}
              value={val}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>
        ))}
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Predict Quality"}
        </button>
      </form>
    </div>
  );
}

export default PredictionForm;