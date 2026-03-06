import { Card, CardContent, Typography } from "@mui/material";

export default function ScoreCard({title, value}) {
  return (
    <Card sx={{ minWidth: 200 }}>
      <CardContent>
        <Typography variant="h6">{title}</Typography>
        <Typography variant="h3">{value}</Typography>
      </CardContent>
    </Card>
  );
}