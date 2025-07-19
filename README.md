# Project NEER - Lake Water Health Monitoring Dashboard

A comprehensive water quality monitoring system for lakes in Coimbatore, India, using satellite imagery and real-time data analysis.

## 🌊 Features

### 🛰️ Satellite Data Integration
- **Google Earth Engine** integration for real satellite data analysis
- **Sentinel-2** imagery processing for water quality assessment
- **Automatic fallback** to mock data for development and reliability

### 📊 Water Quality Monitoring
- **Multi-lake monitoring** for 5 major lakes in Coimbatore
- **Real-time water quality indices**: NDWI, NDCI, FAI, MCI
- **BOD level calculations** and water health assessments
- **Interactive map visualization** with clickable lake polygons

### 📈 Advanced Analytics
- **Historical trend analysis** (2019-2024) with time-series data
- **Trend calculations** (improving/degrading/stable) year-over-year
- **Water quality alerts** for rapidly degrading conditions
- **Pollution source mapping** with catchment area analysis

### 🚨 Alert System
- **Real-time alerts** for water quality degradation
- **Multiple alert types**: BOD changes, algal blooms, high turbidity
- **Severity levels** with recommended actions
- **Detailed pollution source identification**

## 🏗️ Architecture

### Backend (Flask + Python)
- **Flask REST API** with Google Earth Engine integration
- **GeoJSON processing** for lake boundary data
- **Real-time satellite data analysis** with mock data fallback
- **Comprehensive water quality calculations**

### Frontend (React + TypeScript)
- **Modern React application** with TypeScript
- **Material-UI** for consistent design
- **Leaflet maps** for interactive visualization
- **Responsive design** for multiple screen sizes

## 🗺️ Monitored Lakes

1. **Ukkadam Lake** - High pollution risk monitoring
2. **Valankulam** - Improving trend tracking
3. **Kurichi Kulam** - Stable condition monitoring
4. **Perur Lake** - Algal bloom detection
5. **Singanallur Lake** - Urban runoff analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Earth Engine account (optional, mock data available)

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Access the Dashboard
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📋 API Endpoints

- `GET /api/lakes?year={year}` - Get all lakes data for a specific year
- `GET /api/lakes/{id}/history` - Get historical trend data
- `GET /api/alerts` - Get water quality alerts
- `GET /api/pollution-sources/{id}` - Get pollution source mapping

## 🎯 Usage

1. **Dashboard Overview**: View all lakes with current water quality status
2. **Interactive Map**: Click on lake polygons to view detailed information
3. **Historical Trends**: Analyze water quality changes over time
4. **Quality Alerts**: Monitor active alerts and recommended actions
5. **Pollution Mapping**: Identify pollution sources and risk factors

## 🔬 Technical Details

### Water Quality Indices
- **NDWI** (Normalized Difference Water Index): Water detection and quality
- **NDCI** (Normalized Difference Chlorophyll Index): Algae concentration
- **FAI** (Floating Algae Index): Surface algae detection
- **MCI** (Maximum Chlorophyll Index): Chlorophyll concentration

### Data Sources
- **Sentinel-2** satellite imagery via Google Earth Engine
- **GeoJSON** boundary files for lake polygons
- **Historical data** with trend analysis algorithms

## 🛠️ Development

### Project Structure
```
project-neer-dashboard/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── geojson_files/        # Lake boundary data
│       ├── Kurichi kulam.geojson
│       ├── Perur lake.geojson
│       ├── Singanallur lake.geojson
│       ├── ukkadamlakepolygonmap.geojson
│       └── valankulam(includes chinna kulam).geojson
└── frontend/
    ├── package.json          # Node.js dependencies
    ├── public/
    │   └── index.html        # HTML template
    └── src/
        ├── App.tsx           # Main React component
        ├── components/       # React components
        │   ├── MainDashboard.tsx
        │   ├── WaterHealthCard.tsx
        │   ├── AlertsPanel.tsx
        │   ├── HistoricalTrends.tsx
        │   └── PollutionMappingPanel.tsx
        └── services/
            └── apiService.ts # API integration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Earth Engine** for satellite imagery access
- **Copernicus Sentinel-2** data
- **Material-UI** for React components
- **Leaflet** for map visualization

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**Project NEER** - Nurturing Environmental Excellence and Restoration
