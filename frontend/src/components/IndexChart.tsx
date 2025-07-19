import React from "react";
import { Bar } from "react-chartjs-2";
import { Card, CardContent, Typography } from "@mui/material";
import { Lake } from "../services/apiService";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface IndexChartProps {
  lakes: Lake[];
  selectedYear: number;
}

const IndexChart: React.FC<IndexChartProps> = ({ lakes, selectedYear }) => {
  const data = {
    labels: lakes.map((lake) => lake.name),
    datasets: [
      {
        label: "NDWI",
        data: lakes.map((lake) => lake.ndwi),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
      {
        label: "BOD (mg/L)",
        data: lakes.map((lake) => lake.bodLevel),
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: `Water Quality Indices - ${selectedYear}`,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Values",
        },
      },
    },
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Water Quality Analysis
        </Typography>
        <Bar data={data} options={options} />
      </CardContent>
    </Card>
  );
};

export default IndexChart;
