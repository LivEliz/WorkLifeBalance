import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

function StressChart({ data }) {

  const chartData = [
    { name: "Work Hours", value: data.workHours },
    { name: "Sleep Hours", value: data.sleepHours },
    { name: "Stress", value: data.stress }
  ];

  return (

    <BarChart width={400} height={300} data={chartData}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="value" fill="#3b82f6" />
    </BarChart>

  );
}

export default StressChart;