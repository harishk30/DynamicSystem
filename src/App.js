import React, { useState } from 'react';

function App() {
  const [imageUrl, setImageUrl] = useState(null);
  const [timeRange, setTimeRange] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSliderChange = (e) => {
    setTimeRange(parseInt(e.target.value, 10));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const A = [
        [parseFloat(e.target.a11.value), parseFloat(e.target.a12.value)],
        [parseFloat(e.target.a21.value), parseFloat(e.target.a22.value)],
      ];

      const response = await fetch(`https://newdynamicsystem-b87039aabd02.herokuapp.com/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ A, timeRange }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch image');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (error) {
      setError('An error occurred. Please try again.');
    }

    setLoading(false);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h3>System Matrix (A)</h3>
        <input type="number" name="a11" placeholder="A[0][0]" step="0.1" required />
        <input type="number" name="a12" placeholder="A[0][1]" step="0.1" required />
        <input type="number" name="a21" placeholder="A[1][0]" step="0.1" required />
        <input type="number" name="a22" placeholder="A[1][1]" step="0.1" required />

        <h3>Time Range</h3>
        <input type="range" min="1" max="20" value={timeRange} onChange={handleSliderChange} />
        <span>Time Range: {-timeRange / 2} to {timeRange / 2}</span>

        <button type="submit" disabled={loading}>
          {loading ? 'Simulating...' : 'Simulate'}
        </button>
      </form>

      {error && <p>{error}</p>}

      {imageUrl && (
        <div>
          <h3>Phase Portrait</h3>
          <img src={imageUrl} alt="Phase Portrait" />
        </div>
      )}
    </div>
  );
}

export default App;