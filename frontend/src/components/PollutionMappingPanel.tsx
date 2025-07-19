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
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  Factory,
  Home,
  Agriculture,
  Construction,
  LocalShipping,
  Warning,
} from '@mui/icons-material';
import { getPollutionSources, PollutionMapping, Lake } from '../services/apiService';

interface PollutionMappingProps {
  lakes: Lake[];
}

const PollutionMappingPanel: React.FC<PollutionMappingProps> = ({ lakes }) => {
  const [selectedLake, setSelectedLake] = useState<string>('');
  const [pollutionData, setPollutionData] = useState<PollutionMapping | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (lakes.length > 0 && !selectedLake) {
      setSelectedLake(lakes[0].id);
    }
  }, [lakes, selectedLake]);

  useEffect(() => {
    if (selectedLake) {
      fetchPollutionData();
    }
  }, [selectedLake]);

  const fetchPollutionData = async () => {
    if (!selectedLake) return;
    
    try {
      setLoading(true);
      const response = await getPollutionSources(selectedLake);
      setPollutionData(response);
    } catch (error) {
      console.error('Error fetching pollution data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return '#f44336';
      case 'medium':
        return '#ff9800';
      case 'low':
        return '#4caf50';
      default:
        return '#9e9e9e';
    }
  };

  const getSourceIcon = (sourceType: string) => {
    const type = sourceType.toLowerCase();
    if (type.includes('industrial') || type.includes('textile') || type.includes('factory')) {
      return <Factory />;
    } else if (type.includes('urban') || type.includes('residential') || type.includes('sewage')) {
      return <Home />;
    } else if (type.includes('agricultural') || type.includes('farm')) {
      return <Agriculture />;
    } else if (type.includes('construction')) {
      return <Construction />;
    } else {
      return <LocalShipping />;
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (!lakes.length) {
    return (
      <Typography color="textSecondary">
        No lakes available for pollution mapping.
      </Typography>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Pollution Source Mapping
        </Typography>

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

          {pollutionData && (
            <Grid item xs={12} md={6}>
              <Box display="flex" alignItems="center" gap={2}>
                <Typography variant="subtitle1" fontWeight="bold">
                  Risk Level:
                </Typography>
                <Chip
                  icon={<Warning />}
                  label={`${pollutionData.risk_level.toUpperCase()} (${pollutionData.pollution_risk_score}/100)`}
                  color={getRiskColor(pollutionData.risk_level) as any}
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
            ) : pollutionData ? (
              <>
                {/* Risk Score Progress */}
                <Box sx={{ mb: 4 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Pollution Risk Score: {pollutionData.pollution_risk_score}/100
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={pollutionData.pollution_risk_score}
                    color={getRiskColor(pollutionData.risk_level) as any}
                    sx={{ height: 10, borderRadius: 1 }}
                  />
                </Box>

                <Grid container spacing={3}>
                  {/* Catchment Analysis Table */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Catchment Land Use Analysis
                    </Typography>
                    <TableContainer component={Paper}>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Land Use Type</TableCell>
                            <TableCell align="right">Coverage (%)</TableCell>
                            <TableCell align="right">Visual</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          <TableRow>
                            <TableCell>Urban</TableCell>
                            <TableCell align="right">{pollutionData.catchment_analysis.urban_coverage_percent.toFixed(1)}%</TableCell>
                            <TableCell align="right">
                              <LinearProgress
                                variant="determinate"
                                value={pollutionData.catchment_analysis.urban_coverage_percent}
                                color="warning"
                                sx={{ width: 100, height: 8 }}
                              />
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Industrial</TableCell>
                            <TableCell align="right">{pollutionData.catchment_analysis.industrial_coverage_percent.toFixed(1)}%</TableCell>
                            <TableCell align="right">
                              <LinearProgress
                                variant="determinate"
                                value={pollutionData.catchment_analysis.industrial_coverage_percent}
                                color="error"
                                sx={{ width: 100, height: 8 }}
                              />
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Vegetation</TableCell>
                            <TableCell align="right">{pollutionData.catchment_analysis.vegetation_coverage_percent.toFixed(1)}%</TableCell>
                            <TableCell align="right">
                              <LinearProgress
                                variant="determinate"
                                value={pollutionData.catchment_analysis.vegetation_coverage_percent}
                                color="success"
                                sx={{ width: 100, height: 8 }}
                              />
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Water</TableCell>
                            <TableCell align="right">{pollutionData.catchment_analysis.water_coverage_percent.toFixed(1)}%</TableCell>
                            <TableCell align="right">
                              <LinearProgress
                                variant="determinate"
                                value={pollutionData.catchment_analysis.water_coverage_percent}
                                color="info"
                                sx={{ width: 100, height: 8 }}
                              />
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                    
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                      Total Catchment Area: {pollutionData.catchment_analysis.total_area_km2} km²
                    </Typography>
                  </Grid>

                  {/* Pollution Sources */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Identified Pollution Sources
                    </Typography>
                    <List>
                      {pollutionData.identified_sources.map((source, index) => (
                        <ListItem key={index} divider>
                          <ListItemIcon>
                            {getSourceIcon(source.type)}
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Box display="flex" alignItems="center" gap={1}>
                                <Typography variant="body1">
                                  {source.type}
                                </Typography>
                                <Chip
                                  label={source.severity}
                                  size="small"
                                  sx={{
                                    backgroundColor: getSeverityColor(source.severity),
                                    color: 'white',
                                  }}
                                />
                              </Box>
                            }
                            secondary={`Distance: ${source.distance_km} km from lake`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Grid>

                  {/* Recommendations */}
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                      Management Recommendations
                    </Typography>
                    <List>
                      {pollutionData.recommendations.map((recommendation, index) => (
                        <ListItem key={index}>
                          <ListItemText
                            primary={`${index + 1}. ${recommendation}`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Grid>
                </Grid>
              </>
            ) : (
              <Typography color="textSecondary">
                Select a lake to view pollution source analysis.
              </Typography>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default PollutionMappingPanel;
