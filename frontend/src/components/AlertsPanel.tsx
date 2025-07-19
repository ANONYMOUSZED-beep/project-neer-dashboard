import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Alert,
  AlertTitle,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Collapse,
  CircularProgress,
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  ExpandMore,
  ExpandLess,
} from '@mui/icons-material';
import { getWaterQualityAlerts, Alert as AlertType, AlertsResponse } from '../services/apiService';

const AlertsPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<AlertType[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<{ [key: string]: boolean }>({});

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response: AlertsResponse = await getWaterQualityAlerts();
      setAlerts(response.alerts);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return <Error color="error" />;
      case 'medium':
        return <Warning color="warning" />;
      default:
        return <Info color="info" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      default:
        return 'info';
    }
  };

  const toggleExpanded = (alertId: string) => {
    setExpanded(prev => ({
      ...prev,
      [alertId]: !prev[alertId]
    }));
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={2}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Water Quality Alerts ({alerts.length})
        </Typography>
        
        {alerts.length === 0 ? (
          <Typography color="textSecondary">
            No active alerts at this time.
          </Typography>
        ) : (
          <List>
            {alerts.map((alert) => (
              <ListItem key={alert.id} divider>
                <Box sx={{ width: '100%' }}>
                  <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Box display="flex" alignItems="center" gap={1}>
                      {getSeverityIcon(alert.severity)}
                      <Typography variant="subtitle1" fontWeight="bold">
                        {alert.lake_name}
                      </Typography>
                      <Chip
                        label={alert.severity.toUpperCase()}
                        color={getSeverityColor(alert.severity) as any}
                        size="small"
                      />
                    </Box>
                    <IconButton
                      onClick={() => toggleExpanded(alert.id)}
                      size="small"
                    >
                      {expanded[alert.id] ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                  </Box>
                  
                  <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                    {alert.message}
                  </Typography>
                  
                  <Typography variant="caption" color="textSecondary">
                    {formatTimestamp(alert.timestamp)}
                  </Typography>

                  <Collapse in={expanded[alert.id]}>
                    <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                      {alert.current_bod && alert.previous_bod && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold">
                            BOD Level Change:
                          </Typography>
                          <Typography variant="body2">
                            Previous: {alert.previous_bod} mg/L → Current: {alert.current_bod} mg/L
                            {alert.change && ` (${alert.change > 0 ? '+' : ''}${alert.change} mg/L)`}
                          </Typography>
                        </Box>
                      )}
                      
                      <Typography variant="body2" fontWeight="bold">
                        Recommended Action:
                      </Typography>
                      <Typography variant="body2">
                        {alert.recommended_action}
                      </Typography>
                    </Box>
                  </Collapse>
                </Box>
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
};

export default AlertsPanel;
