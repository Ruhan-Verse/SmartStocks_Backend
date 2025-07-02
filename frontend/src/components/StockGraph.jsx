// 📦 Dependencies: Chart.js & react-chartjs-2
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

// Register chart components
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const StockGraph = ({ data, title }) => {
  if (!data || !data.labels || !data.values) return null;

  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: title || 'Stock Price',
        data: data.values,
        fill: false,
        borderColor: 'rgba(75, 192, 192, 1)',
        tension: 0.3,
        pointRadius: 3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
    },
    scales: {
      y: { beginAtZero: false },
    },
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default StockGraph;
