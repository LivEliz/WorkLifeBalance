import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function TrendChart() {

  const data = {
    labels: ["Week1", "Week2", "Week3", "Week4"],
    datasets: [
      {
        label: "Balance Score",
        data: [70, 65, 60, 64],
        borderColor: "blue"
      }
    ]
  };

  return <Line data={data} />;
}

export default TrendChart;