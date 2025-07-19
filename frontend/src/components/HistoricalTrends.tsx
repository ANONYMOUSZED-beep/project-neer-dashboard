import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  CircularProgress,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
} from '@mui/material';
import { getLakeHistory, HistoricalResponse, Lake } from '../services/apiService';

interface HistoricalTrendsProps {
  lakes: Lake[];
}

const HistoricalTrends: React.FC<HistoricalTrendsProps> = ({ lakes }) => {
  const [selectedLake, setSelectedLake] = useState<string>('');
  const [historicalData, setHistoricalData] = useState<HistoricalResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (lakes.length > 0 && !selectedLake) {
      setSelectedLake(lakes[0].id);
    }
  }, [lakes, selectedLake]);

  useEffect(() => {
    if (selectedLake) {
      fetchHistoricalData();
    }
  }, [selectedLake]);

  const fetchHistoricalData = async () => {
    if (!selectedLake) return;
    
    try {
      setLoading(true);
      const response = await getLakeHistory(selectedLake, 2019, 2024);
      setHistoricalData(response);
    } catch (error) {
      console.error('Error fetching historical data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'improving':
        return 'success';
      case 'degrading':
        return 'error';
      case 'stable':
        return 'info';
      default:
        return 'default';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'improving':
        return '↗️';
      case 'degrading':
        return '↘️';
      case 'stable':
        return '→';
      default:
        return '📊';
    }
  };

  if (!lakes.length) {
    return (
      <Typography color="textSecondary">
        No lakes available for historical analysis.
      </Typography>
    );
  }

  return (
    <Card>
      <CardContent>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Select Lake</InputLabel>
              <Select
                value={selectedLake}
                onChange={(e) => setSelectedLake(e.target.value)}
                label="Select Lake"
              >
                {lakes.map((lake) => (
                  <MenuItem key={lake.id} value={lake.id}>
                    {lake.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {historicalData && (
            <Grid item xs={12} md={6}>
              <Box display="flex" alignItems="center" gap={2}>
                <Typography variant="h6">
                  Overall Trend:
                </Typography>
                <Chip
                  label={`${getTrendIcon(historicalData.trend_analysis.overall_trend)} ${historicalData.trend_analysis.overall_trend.toUpperCase()}`}
                  color={getTrendColor(historicalData.trend_analysis.overall_trend) as any}
                  variant="outlined"
                />
              </Box>
            </Grid>
          )}

          <Grid item xs={12}>
            {loading ? (
              <Box display="flex" justifyContent="center" p={4}>
                <CircularProgress />
              </Box>
            ) : historicalData ? (
              <>
                {/* BOD Level Trend Table */}
                <Box sx={{ mb: 4 }}>
                  <Typography variant="h6" gutterBottom>
                    Historical Water Quality Data
                  </Typography>
                  <TableContainer component={Paper}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Year</TableCell>
                          <TableCell align="right">BOD Level (mg/L)</TableCell>
                          <TableCell align="right">NDWI</TableCell>
                          <TableCell align="right">Water Health</TableCell>
                          <TableCell align="center">Trend</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {historicalData.historical_data.map((row) => (
                          <TableRow key={row.year}>
                            <TableCell>{row.year}</TableCell>
                            <TableCell align="right">{row.bodLevel.toFixed(2)}</TableCell>
                            <TableCell align="right">{row.ndwi.toFixed(4)}</TableCell>
                            <TableCell align="right">
                              <Chip
                                label={row.waterHealth}
                                color={
                                  row.waterHealth === 'Good' ? 'success' :
                                  row.waterHealth === 'Moderate' ? 'warning' : 'error'
                                }
                                size="small"
                              />
                            </TableCell>
                            <TableCell align="center">
                              <Chip
                                label={`${getTrendIcon(row.trend)} ${row.trend}`}
                                color={getTrendColor(row.trend) as any}
                                size="small"
                                variant="outlined"
                              />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>

                {/* Visual BOD Trend */}
                <Box sx={{ mb: 4 }}>
                  <Typography variant="h6" gutterBottom>
                    BOD Level Trend Visualization
                  </Typography>
                  {historicalData.historical_data.map((data, index) => (
                    <Box key={data.year} sx={{ mb: 2 }}>
                      <Box display="flex" justifyContent="space-between" alignItems="center">
                        <Typography variant="body2">
                          {data.year}: {data.bodLevel.toFixed(2)} mg/L
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {data.waterHealth}
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={Math.min(100, (data.bodLevel / 20) * 100)}
                        color={
                          data.bodLevel > 10 ? 'error' :
                          data.bodLevel > 5 ? 'warning' : 'success'
                        }
                        sx={{ height: 8, borderRadius: 1 }}
                      />
                    </Box>
                  ))}
                </Box>

                {/* Trend Analysis Summary */}
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Trend Analysis Summary
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={4}>
                      <Card variant="outlined">
                        <CardContent sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" color="success.main">
                            {historicalData.trend_analysis.trend_counts.improving}
                          </Typography>
                          <Typography variant="body2">
                            Improving Years
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card variant="outlined">
                        <CardContent sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" color="info.main">
                            {historicalData.trend_analysis.trend_counts.stable}
                          </Typography>
                          <Typography variant="body2">
                            Stable Years
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card variant="outlined">
                        <CardContent sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" color="error.main">
                            {historicalData.trend_analysis.trend_counts.degrading}
                          </Typography>
                          <Typography variant="body2">
                            Degrading Years
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Box>
              </>
            ) : (
              <Typography color="textSecondary">
                Select a lake to view historical trends.
              </Typography>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default HistoricalTrends;
