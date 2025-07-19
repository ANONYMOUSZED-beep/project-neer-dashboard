import React from "react";
import { Card, CardContent, Typography, Chip, Box } from "@mui/material";
import { Water, Warning, CheckCircle } from "@mui/icons-material";
import { Lake } from "../services/apiService";

interface WaterHealthCardProps {
  lake: Lake;
}

const WaterHealthCard: React.FC<WaterHealthCardProps> = ({ lake }) => {
  const getHealthColor = (health: string) => {
    const colors = {
      Excellent: "#1e40af",
      Good: "#3b82f6",
      Moderate: "#eab308",
      Poor: "#f97316",
      "Very Poor": "#dc2626",
    };
    return colors[health as keyof typeof colors] || "#6b7280";
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Water sx={{ mr: 1, color: getHealthColor(lake.waterHealth) }} />
          <Typography variant="h5">{lake.name}</Typography>
        </Box>

        <Box mb={2}>
          <Chip
            label={lake.waterHealth}
            style={{
              backgroundColor: getHealthColor(lake.waterHealth),
              color: "white",
              fontWeight: "bold",
            }}
          />
        </Box>

        <Typography variant="body1" gutterBottom>
          <strong>NDWI:</strong> {lake.ndwi.toFixed(4)}
        </Typography>

        <Typography variant="body1" gutterBottom>
          <strong>BOD Level:</strong> {lake.bodLevel.toFixed(2)} mg/L
        </Typography>

        <Box mt={2}>
          <Typography variant="h6" gutterBottom>
            <Warning sx={{ mr: 1, color: "#f97316" }} />
            Pollution Causes
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {lake.pollutionCauses}
          </Typography>
        </Box>

        <Box mt={2}>
          <Typography variant="h6" gutterBottom>
            <CheckCircle sx={{ mr: 1, color: "#10b981" }} />
            AI Suggestions
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {lake.suggestions}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default WaterHealthCard;
