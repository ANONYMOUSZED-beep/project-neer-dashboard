import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import { Water } from "@mui/icons-material";

const Navigation: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box display="flex" alignItems="center">
          <Water sx={{ mr: 2 }} />
          <Typography variant="h6" component="div">
            Project NEER - Water Quality Dashboard
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;
