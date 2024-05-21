import React, { useState } from 'react';
import Plot from 'react-plotly.js';

function App() {
    const [data, setData] = useState(null);

    const handleSubmit = async (e) => {
      e.preventDefault();
      
      // Collecting form input values
      const A = [
          [parseFloat(e.target.a11.value), parseFloat(e.target.a12.value)],
          [parseFloat(e.target.a21.value), parseFloat(e.target.a22.value)],
      ];
      const time = parseInt(e.target.time.value, 10);

      // Sending POST request to the Flask backend
      const response = await fetch('http://127.0.0.1:5000/simulate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ A, time }),
      });

      const result = await response.json();

      setData(result);
  };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <h3>System Matrix (A)</h3>
                <input type="text" name="a11" placeholder="A[0][0]" required />
                <input type="text" name="a12" placeholder="A[0][1]" required />
                <input type="text" name="a21" placeholder="A[1][0]" required />
                <input type="text" name="a22" placeholder="A[1][1]" required />
                <h3>Time Duration</h3>
                <input type="text" name="time" placeholder="time" required />
                <button type="submit">Simulate</button>
            </form>
            {data && (
                <Plot
                    data={data.trajectories.map((trajectory, index) => ({
                        x: trajectory[0],
                        y: trajectory[1],
                        type: 'scatter',
                        mode: 'points',
                        name: `Trajectory ${index + 1}`,
                    }))}
                    layout={{ title: 'Phase Portrait' }}
                />
            )}
        </div>
    );
}

export default App;
