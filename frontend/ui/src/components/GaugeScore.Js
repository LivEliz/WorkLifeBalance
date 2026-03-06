import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

const data = [
  { week: "Week 1", score: 60 },
  { week: "Week 2", score: 70 },
  { week: "Week 3", score: 75 },
  { week: "Week 4", score: 82 }
];

export default function TrendChart() {
  return (
    <LineChart width={500} height={300} data={data}>
      <XAxis dataKey="week" />
      <YAxis />
      <Tooltip />
      <CartesianGrid stroke="#ccc" />
      <Line type="monotone" dataKey="score" stroke="#3b82f6"/>
    </LineChart>
  );
}