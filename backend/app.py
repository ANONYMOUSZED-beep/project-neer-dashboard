from flask import Flask, jsonify, request
from flask_cors import CORS
import ee
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize Google Earth Engine
def initialize_earth_engine():
    """Initialize Google Earth Engine with proper authentication"""
    try:
        # Try to initialize with service account
        ee.Initialize(project='neer2025')
        print("Google Earth Engine initialized successfully with existing credentials")
        return True
    except Exception as e:
        print(f"Standard initialization failed: {e}")
        try:
            # Try to authenticate interactively
            ee.Authenticate()
            ee.Initialize(project='neer2025')
            print("Google Earth Engine initialized successfully after authentication")
            return True
        except Exception as auth_error:
            print(f"Earth Engine authentication failed: {auth_error}")
            print("Will use mock data as fallback")
            return False

# Global variable to track EE status
EE_INITIALIZED = initialize_earth_engine()

@app.route('/')
def home():
    """Simple test route"""
    return jsonify({"message": "NEER Dashboard API is running!", "status": "success"})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/test')
def test_endpoint():
    """Test endpoint without Earth Engine"""
    return jsonify({
        "message": "API is working",
        "lakes_available": ["Ukkadam", "Valankulam", "Kurichi", "Perur", "Singanallur"],
        "status": "success"
    })

@app.route('/api/lakes/mock', methods=['GET'])
def get_mock_lakes():
    """Get mock lake data for testing"""
    year = request.args.get('year', 2024, type=int)
    
    mock_lakes = [
        {
            'id': 'ukkadam',
            'name': 'Ukkadam',
            'ndwi': 0.3,
            'ndci': -0.1,
            'fai': 0.02,
            'mci': 15.2,
            'swir_ratio': 1.2,
            'turbidity': 850.5,
            'bodLevel': 15.45,
            'waterHealth': 'Poor',
            'pollutionCauses': 'High sediment, algal bloom',
            'suggestions': 'Reduce catchment erosion, limit nutrient runoff',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Ukkadam"},
                    "geometry": {
                        "coordinates": [[[76.96095638648234, 10.988575303133587], [76.96051032283168, 10.988737482780266], [76.95813131669479, 10.9880238916666], [76.96095638648234, 10.988575303133587]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'valankulam',
            'name': 'Valankulam',
            'ndwi': 0.5,
            'ndci': -0.05,
            'fai': 0.01,
            'mci': 8.1,
            'swir_ratio': 1.0,
            'turbidity': 420.3,
            'bodLevel': 6.2,
            'waterHealth': 'Moderate',
            'pollutionCauses': 'Minor algal growth',
            'suggestions': 'Monitor nutrient levels',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Valankulam"},
                    "geometry": {
                        "coordinates": [[[76.95, 10.97], [76.96, 10.97], [76.96, 10.98], [76.95, 10.98], [76.95, 10.97]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'kurichi',
            'name': 'Kurichi',
            'ndwi': 0.7,
            'ndci': -0.15,
            'fai': 0.005,
            'mci': 5.3,
            'swir_ratio': 0.8,
            'turbidity': 180.1,
            'bodLevel': 3.8,
            'waterHealth': 'Good',
            'pollutionCauses': 'No major issues',
            'suggestions': 'Continue current management',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Kurichi"},
                    "geometry": {
                        "coordinates": [[[76.94, 10.99], [76.95, 10.99], [76.95, 11.00], [76.94, 11.00], [76.94, 10.99]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        }
    ]
    
    return jsonify(mock_lakes)

def load_lakes_from_files():
    """Load all lake geometries from GeoJSON files"""
    lakes = {}
    
    # Ukkadam geometry (hardcoded from your original code)
    ukkadam_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"name": "Ukkadam"},
            "geometry": {
                "coordinates": [[[76.96095638648234, 10.988575303133587], 
                               [76.96051032283168, 10.988737482780266],
                               [76.95813131669479, 10.9880238916666], 
                               [76.95646270822363, 10.987018373985165],
                               [76.9540010977073, 10.985866889852815], 
                               [76.9518864255856, 10.985218164418924],
                               [76.9500856501075, 10.984958673846393], 
                               [76.94997000397598, 10.983920709273917],
                               [76.94919352280618, 10.983223324777526], 
                               [76.94821879112538, 10.982947614174023],
                               [76.94826835375284, 10.98236375557407], 
                               [76.94702928805697, 10.981925860866397],
                               [76.94699624630488, 10.980417551902818], 
                               [76.9468640792968, 10.9802391492576],
                               [76.94574065973245, 10.980222930829356], 
                               [76.94504678294214, 10.980093183376937],
                               [76.94524503345434, 10.979120075661697], 
                               [76.94600499374752, 10.9791038571732],
                               [76.9466327870337, 10.978730831677623], 
                               [76.94874745915558, 10.978925453734405],
                               [76.94957350295277, 10.979249823542816], 
                               [76.95020129623902, 10.979055201699836],
                               [76.95033346324595, 10.97866595763135], 
                               [76.95153948719098, 10.97843889835319],
                               [76.95226640573219, 10.978649739116705], 
                               [76.95350547142806, 10.978682176143948],
                               [76.95411674383888, 10.97847133540364], 
                               [76.95580187318546, 10.978422679827219],
                               [76.95813131669479, 10.977952342171605], 
                               [76.95958515377828, 10.978714613167696],
                               [76.96034511407152, 10.979266042023383], 
                               [76.96084074034962, 10.97997965430892],
                               [76.96128680400022, 10.983077360372121], 
                               [76.96130332487684, 10.984974892013383],
                               [76.96117115786876, 10.985493872901799], 
                               [76.9612702831248, 10.986029070987911],
                               [76.96095638648234, 10.988575303133587]]],
                "type": "Polygon"
            }
        }]
    }
    
    lakes["Ukkadam"] = ee.FeatureCollection(ukkadam_geojson)
    
    # Load other lakes from files
    lake_files = {
        "Valankulam": "geojson_files/valankulam(includes chinna kulam).geojson",
        "Kurichi": "geojson_files/Kurichi kulam.geojson",
        "Perur": "geojson_files/Perur lake.geojson",
        "Singanallur": "geojson_files/Singanallur lake.geojson"
    }
    
    for lake_name, filename in lake_files.items():
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    geojson_data = json.load(f)
                    lakes[lake_name] = ee.FeatureCollection(geojson_data)
            except Exception as e:
                print(f"Error loading {lake_name}: {str(e)}")
                continue
    
    return lakes

def compute_indices(image):
    """Compute all water quality indices"""
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    ndci = image.normalizedDifference(['B5', 'B4']).rename('NDCI')
    fai = image.expression(
        '(B8 - B4) / (B8 + B4)',
        {'B8': image.select('B8'), 'B4': image.select('B4')}
    ).rename('FAI')
    mci = image.expression(
        'B5 - B4 - (B6 - B4) * ((705 - 665) / (740 - 665))',
        {'B5': image.select('B5'), 'B4': image.select('B4'), 'B6': image.select('B6')}
    ).rename('MCI')
    turbidity = image.select(['B2', 'B3', 'B4']).reduce(ee.Reducer.mean()).rename('Turbidity')
    swir_ratio = image.select('B11').divide(image.select('B12')).rename('SWIR_Ratio')
    return image.addBands([ndwi, ndci, fai, mci, turbidity, swir_ratio])

def classify_pollution(values):
    """Classify pollution causes and generate suggestions"""
    reasons = []
    suggestions = []

    if values.get('FAI', 0) > 0.05:
        reasons.append("Algal bloom")
        suggestions.append("Limit nutrient runoff")

    if values.get('NDWI', 0) < 0.2:
        reasons.append("Water scarcity")
        suggestions.append("Increase water inflow")

    if values.get('SWIR_Ratio', 0) > 1.5:
        reasons.append("Chemical or sediment pollution")
        suggestions.append("Investigate industrial discharges")

    if values.get('Turbidity', 0) > 1000:
        reasons.append("High sediment or garbage dumping")
        suggestions.append("Reduce catchment erosion / waste dumping")

    return ", ".join(reasons) or "No major issues", ", ".join(set(suggestions)) or "No action needed"

def get_mock_lakes_response(year):
    """Return mock data response for testing when Earth Engine is not available"""
    mock_lakes = [
        {
            'id': 'ukkadam',
            'name': 'Ukkadam',
            'ndwi': 0.3,
            'ndci': -0.1,
            'fai': 0.02,
            'mci': 15.2,
            'swir_ratio': 1.2,
            'turbidity': 850.5,
            'bodLevel': 15.45,
            'waterHealth': 'Poor',
            'pollutionCauses': 'High sediment, algal bloom',
            'suggestions': 'Reduce catchment erosion, limit nutrient runoff',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Ukkadam"},
                    "geometry": {
                        "coordinates": [[[76.96095638648234, 10.988575303133587], [76.96051032283168, 10.988737482780266], [76.95813131669479, 10.9880238916666], [76.96095638648234, 10.988575303133587]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'valankulam',
            'name': 'Valankulam',
            'ndwi': 0.5,
            'ndci': -0.05,
            'fai': 0.01,
            'mci': 8.1,
            'swir_ratio': 1.0,
            'turbidity': 420.3,
            'bodLevel': 6.2,
            'waterHealth': 'Moderate',
            'pollutionCauses': 'Minor algal growth',
            'suggestions': 'Monitor nutrient levels',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Valankulam"},
                    "geometry": {
                        "coordinates": [[[76.95, 10.97], [76.96, 10.97], [76.96, 10.98], [76.95, 10.98], [76.95, 10.97]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'kurichi',
            'name': 'Kurichi',
            'ndwi': 0.7,
            'ndci': -0.15,
            'fai': 0.005,
            'mci': 5.3,
            'swir_ratio': 0.8,
            'turbidity': 180.1,
            'bodLevel': 3.8,
            'waterHealth': 'Good',
            'pollutionCauses': 'No major issues',
            'suggestions': 'Continue current management',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Kurichi"},
                    "geometry": {
                        "coordinates": [[[76.94, 10.99], [76.95, 10.99], [76.95, 11.00], [76.94, 11.00], [76.94, 10.99]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'perur',
            'name': 'Perur',
            'ndwi': 0.4,
            'ndci': -0.08,
            'fai': 0.015,
            'mci': 12.5,
            'swir_ratio': 1.1,
            'turbidity': 650.2,
            'bodLevel': 8.1,
            'waterHealth': 'Poor',
            'pollutionCauses': 'Chemical pollution, sediment',
            'suggestions': 'Investigate industrial discharges, reduce erosion',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Perur"},
                    "geometry": {
                        "coordinates": [[[76.93, 10.96], [76.94, 10.96], [76.94, 10.97], [76.93, 10.97], [76.93, 10.96]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        },
        {
            'id': 'singanallur',
            'name': 'Singanallur',
            'ndwi': 0.6,
            'ndci': -0.12,
            'fai': 0.008,
            'mci': 6.8,
            'swir_ratio': 0.9,
            'turbidity': 320.4,
            'bodLevel': 5.3,
            'waterHealth': 'Moderate',
            'pollutionCauses': 'Moderate nutrient loading',
            'suggestions': 'Control agricultural runoff',
            'geometry': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Singanallur"},
                    "geometry": {
                        "coordinates": [[[76.97, 10.98], [76.98, 10.98], [76.98, 10.99], [76.97, 10.99], [76.97, 10.98]]],
                        "type": "Polygon"
                    }
                }]
            },
            'year': year
        }
    ]
    
    return jsonify(mock_lakes)

@app.route('/api/lakes', methods=['GET'])
def get_all_lakes():
    """Get all lakes with current water quality data"""
    year = request.args.get('year', 2024, type=int)
    
    # Validate year
    if year < 2015 or year > 2025:
        return jsonify({'error': 'Invalid year. Please use years between 2015-2025'}), 400
    
    try:
        print(f"Attempting to get real data for year {year}")
        lakes = load_lakes_from_files()
        print(f"Loaded {len(lakes)} lakes from files")
        
        # Try to get Sentinel-2 data
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        s2 = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterDate(start, end) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
            .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B8', 'B11', 'B12']) \
            .median()
        
        s2 = compute_indices(s2)
        
        results = []
        
        for lake_name, lake_fc in lakes.items():
            try:
                print(f"Processing lake: {lake_name}")
                # Get lake statistics
                stats = s2.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=lake_fc.geometry(),
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                if stats and 'NDWI' in stats and stats['NDWI'] is not None:
                    # Calculate BOD
                    bod = 26.303 * stats['NDWI'] + 7.546
                    
                    # Classify water health
                    if bod > 8:
                        health = "Poor"
                    elif bod > 4:
                        health = "Moderate"
                    else:
                        health = "Good"
                    
                    # Get pollution causes and suggestions
                    reasons, suggestions = classify_pollution(stats)
                    
                    # Get lake geometry for frontend
                    geometry = lake_fc.getInfo()
                    
                    results.append({
                        'id': lake_name.lower().replace(' ', '_'),
                        'name': lake_name,
                        'ndwi': round(stats.get('NDWI', 0), 4),
                        'ndci': round(stats.get('NDCI', 0), 4),
                        'fai': round(stats.get('FAI', 0), 4),
                        'mci': round(stats.get('MCI', 0), 4),
                        'swir_ratio': round(stats.get('SWIR_Ratio', 0), 4),
                        'turbidity': round(stats.get('Turbidity', 0), 2),
                        'bodLevel': round(bod, 2),
                        'waterHealth': health,
                        'pollutionCauses': reasons,
                        'suggestions': suggestions,
                        'geometry': geometry,
                        'year': year
                    })
                    print(f"Successfully processed {lake_name}")
                else:
                    print(f"No valid stats for {lake_name}")
                    
            except Exception as e:
                print(f"Error processing lake {lake_name}: {str(e)}")
                continue
        
        if results:
            print(f"Returning {len(results)} real lake results")
            return jsonify(results)
        else:
            print("No real data available, falling back to mock data")
            return get_mock_lakes_response(year)
        
    except Exception as e:
        print(f"Earth Engine error: {str(e)}")
        print("Falling back to mock data due to Earth Engine issues")
        return get_mock_lakes_response(year)

@app.route('/api/lakes/<lake_id>/history', methods=['GET'])
def get_lake_history(lake_id):
    """Get historical data for a specific lake with trend analysis"""
    start_year = request.args.get('start_year', 2020, type=int)
    end_year = request.args.get('end_year', 2024, type=int)
    
    # Validate year range
    if start_year > end_year or start_year < 2015 or end_year > 2025:
        return jsonify({'error': 'Invalid year range. Please use years between 2015-2025'}), 400
    
    try:
        # Map lake_id to actual lake names
        lake_mapping = {
            'ukkadam': 'Ukkadam',
            'valankulam': 'Valankulam',
            'kurichi': 'Kurichi',
            'perur': 'Perur',
            'singanallur': 'Singanallur'
        }
        
        lake_name = lake_mapping.get(lake_id.lower())
        
        if not lake_name:
            return jsonify({'error': 'Lake not found'}), 404

        if EE_INITIALIZED:
            return get_real_historical_data(lake_name, start_year, end_year)
        else:
            return get_mock_historical_data(lake_id, start_year, end_year)
        
    except Exception as e:
        print(f"Error in get_lake_history: {str(e)}")
        return get_mock_historical_data(lake_id, start_year, end_year)

def get_real_historical_data(lake_name, start_year, end_year):
    """Get real historical data from Earth Engine"""
    try:
        lakes = load_lakes_from_files()
        
        if lake_name not in lakes:
            return jsonify({'error': 'Lake not found'}), 404
        
        lake_fc = lakes[lake_name]
        historical_data = []
        trend_analysis = {"improving": 0, "degrading": 0, "stable": 0}
        
        previous_bod = None
        
        for year in range(start_year, end_year + 1):
            try:
                start = f"{year}-01-01"
                end_date = f"{year}-12-31"
                s2 = ee.ImageCollection("COPERNICUS/S2_SR") \
                    .filterDate(start, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
                    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B8', 'B11', 'B12']) \
                    .median()
                
                s2 = compute_indices(s2)
                
                stats = s2.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=lake_fc.geometry(),
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                if stats and 'NDWI' in stats and stats['NDWI'] is not None:
                    bod = 26.303 * stats['NDWI'] + 7.546
                    health = "Poor" if bod > 8 else "Moderate" if bod > 4 else "Good"
                    
                    # Trend analysis
                    if previous_bod is not None:
                        if bod < previous_bod - 1:
                            trend = "improving"
                            trend_analysis["improving"] += 1
                        elif bod > previous_bod + 1:
                            trend = "degrading"
                            trend_analysis["degrading"] += 1
                        else:
                            trend = "stable"
                            trend_analysis["stable"] += 1
                    else:
                        trend = "baseline"
                    
                    historical_data.append({
                        'year': year,
                        'ndwi': round(stats['NDWI'], 4),
                        'ndci': round(stats.get('NDCI', 0), 4),
                        'fai': round(stats.get('FAI', 0), 4),
                        'mci': round(stats.get('MCI', 0), 4),
                        'bodLevel': round(bod, 2),
                        'waterHealth': health,
                        'trend': trend,
                        'turbidity': round(stats.get('Turbidity', 0), 2),
                        'swir_ratio': round(stats.get('SWIR_Ratio', 0), 4)
                    })
                    
                    previous_bod = bod
                    
            except Exception as e:
                print(f"Error processing year {year}: {str(e)}")
                continue
        
        # Calculate overall trend
        if trend_analysis["degrading"] > trend_analysis["improving"]:
            overall_trend = "degrading"
        elif trend_analysis["improving"] > trend_analysis["degrading"]:
            overall_trend = "improving"
        else:
            overall_trend = "stable"
        
        return jsonify({
            'historical_data': historical_data,
            'trend_analysis': {
                'overall_trend': overall_trend,
                'trend_counts': trend_analysis,
                'data_points': len(historical_data)
            }
        })
        
    except Exception as e:
        print(f"Error in get_real_historical_data: {str(e)}")
        return get_mock_historical_data(lake_name.lower(), start_year, end_year)

def get_mock_historical_data(lake_id, start_year, end_year):
    """Generate mock historical data with realistic trends"""
    import random
    
    # Base values for different lakes
    base_values = {
        'ukkadam': {'base_ndwi': 0.3, 'trend': -0.02},  # Degrading
        'valankulam': {'base_ndwi': 0.5, 'trend': 0.01},  # Improving
        'kurichi': {'base_ndwi': 0.7, 'trend': 0.005},   # Stable/Improving
        'perur': {'base_ndwi': 0.4, 'trend': -0.015},    # Degrading
        'singanallur': {'base_ndwi': 0.6, 'trend': 0.008} # Improving
    }
    
    lake_config = base_values.get(lake_id, {'base_ndwi': 0.5, 'trend': 0})
    historical_data = []
    trend_analysis = {"improving": 0, "degrading": 0, "stable": 0}
    previous_bod = None
    
    for i, year in enumerate(range(start_year, end_year + 1)):
        # Calculate NDWI with trend and some random variation
        ndwi = lake_config['base_ndwi'] + (lake_config['trend'] * i) + random.uniform(-0.05, 0.05)
        ndwi = max(0, min(1, ndwi))  # Clamp between 0 and 1
        
        bod = 26.303 * ndwi + 7.546
        health = "Poor" if bod > 8 else "Moderate" if bod > 4 else "Good"
        
        # Trend analysis
        if previous_bod is not None:
            if bod < previous_bod - 1:
                trend = "improving"
                trend_analysis["improving"] += 1
            elif bod > previous_bod + 1:
                trend = "degrading"
                trend_analysis["degrading"] += 1
            else:
                trend = "stable"
                trend_analysis["stable"] += 1
        else:
            trend = "baseline"
        
        historical_data.append({
            'year': year,
            'ndwi': round(ndwi, 4),
            'ndci': round(random.uniform(-0.2, 0.1), 4),
            'fai': round(random.uniform(0, 0.05), 4),
            'mci': round(random.uniform(5, 20), 2),
            'bodLevel': round(bod, 2),
            'waterHealth': health,
            'trend': trend,
            'turbidity': round(random.uniform(100, 1000), 2),
            'swir_ratio': round(random.uniform(0.8, 1.5), 4)
        })
        
        previous_bod = bod
    
    # Calculate overall trend
    if trend_analysis["degrading"] > trend_analysis["improving"]:
        overall_trend = "degrading"
    elif trend_analysis["improving"] > trend_analysis["degrading"]:
        overall_trend = "improving"
    else:
        overall_trend = "stable"
    
    return jsonify({
        'historical_data': historical_data,
        'trend_analysis': {
            'overall_trend': overall_trend,
            'trend_counts': trend_analysis,
            'data_points': len(historical_data)
        }
    })

@app.route('/api/alerts', methods=['GET'])
def get_water_quality_alerts():
    """Get water quality alerts for rapidly degrading lakes"""
    try:
        # Check if Earth Engine is available (similar check as other endpoints)
        try:
            ee.Number(1).getInfo()
            return get_real_alerts()
        except:
            return get_mock_alerts()
    except Exception as e:
        print(f"Error in get_water_quality_alerts: {str(e)}")
        return get_mock_alerts()

def get_real_alerts():
    """Get real alerts based on Earth Engine data"""
    try:
        lakes = load_lakes_from_files()
        alerts = []
        
        current_year = 2024
        
        for lake_name, lake_fc in lakes.items():
            try:
                # Get recent data (last 2 years)
                start = f"{current_year-1}-01-01"
                end_date = f"{current_year}-12-31"
                
                s2 = ee.ImageCollection("COPERNICUS/S2_SR") \
                    .filterDate(start, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
                    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B8', 'B11', 'B12'])
                
                # Get data for last year and current year
                last_year = s2.filterDate(f"{current_year-1}-01-01", f"{current_year-1}-12-31").median()
                current_year_data = s2.filterDate(f"{current_year}-01-01", f"{current_year}-12-31").median()
                
                last_year = compute_indices(last_year)
                current_year_data = compute_indices(current_year_data)
                
                # Get statistics
                last_stats = last_year.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=lake_fc.geometry(),
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                current_stats = current_year_data.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=lake_fc.geometry(),
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                if (last_stats and current_stats and 
                    'NDWI' in last_stats and 'NDWI' in current_stats and
                    last_stats['NDWI'] is not None and current_stats['NDWI'] is not None):
                    
                    last_bod = 26.303 * last_stats['NDWI'] + 7.546
                    current_bod = 26.303 * current_stats['NDWI'] + 7.546
                    
                    bod_change = current_bod - last_bod
                    
                    # Generate alerts based on various criteria
                    if bod_change > 3:  # Significant increase in BOD
                        alerts.append({
                            'id': f"alert_{lake_name}_{current_year}",
                            'lake_name': lake_name.title(),
                            'alert_type': 'degrading_water_quality',
                            'severity': 'high' if bod_change > 5 else 'medium',
                            'message': f"Water quality rapidly degrading. BOD increased by {bod_change:.1f} mg/L",
                            'timestamp': f"{current_year}-12-01T00:00:00Z",
                            'current_bod': round(current_bod, 2),
                            'previous_bod': round(last_bod, 2),
                            'change': round(bod_change, 2),
                            'recommended_action': 'Immediate investigation and pollution source assessment required'
                        })
                    
                    # Additional pollution indicators
                    if current_stats.get('NDCI', 0) > 0.2:  # High algae
                        alerts.append({
                            'id': f"algae_{lake_name}_{current_year}",
                            'lake_name': lake_name.title(),
                            'alert_type': 'algal_bloom',
                            'severity': 'medium',
                            'message': f"Potential algal bloom detected (NDCI: {current_stats['NDCI']:.3f})",
                            'timestamp': f"{current_year}-11-15T00:00:00Z",
                            'recommended_action': 'Monitor nutrient levels and implement algae control measures'
                        })
                    
                    if current_stats.get('Turbidity', 0) > 800:  # High turbidity
                        alerts.append({
                            'id': f"turbidity_{lake_name}_{current_year}",
                            'lake_name': lake_name.title(),
                            'alert_type': 'high_turbidity',
                            'severity': 'medium',
                            'message': f"High turbidity detected ({current_stats['Turbidity']:.1f} NTU)",
                            'timestamp': f"{current_year}-11-20T00:00:00Z",
                            'recommended_action': 'Check for erosion sources and sediment runoff'
                        })
                        
            except Exception as e:
                print(f"Error processing alerts for {lake_name}: {str(e)}")
                continue
        
        return jsonify({
            'alerts': alerts,
            'total_alerts': len(alerts),
            'last_updated': f"{current_year}-12-01T00:00:00Z"
        })
        
    except Exception as e:
        print(f"Error in get_real_alerts: {str(e)}")
        return get_mock_alerts()

def get_mock_alerts():
    """Generate mock alerts for demonstration"""
    alerts = [
        {
            'id': 'alert_ukkadam_2024',
            'lake_name': 'Ukkadam Lake',
            'alert_type': 'degrading_water_quality',
            'severity': 'high',
            'message': 'Water quality rapidly degrading. BOD increased by 4.2 mg/L in past year',
            'timestamp': '2024-11-25T08:30:00Z',
            'current_bod': 12.5,
            'previous_bod': 8.3,
            'change': 4.2,
            'recommended_action': 'Immediate investigation and pollution source assessment required'
        },
        {
            'id': 'algae_perur_2024',
            'lake_name': 'Perur Lake',
            'alert_type': 'algal_bloom',
            'severity': 'medium',
            'message': 'Potential algal bloom detected (NDCI: 0.245)',
            'timestamp': '2024-11-20T14:15:00Z',
            'recommended_action': 'Monitor nutrient levels and implement algae control measures'
        },
        {
            'id': 'turbidity_singanallur_2024',
            'lake_name': 'Singanallur Lake',
            'alert_type': 'high_turbidity',
            'severity': 'medium',
            'message': 'High turbidity detected (850.3 NTU)',
            'timestamp': '2024-11-18T11:45:00Z',
            'recommended_action': 'Check for erosion sources and sediment runoff'
        },
        {
            'id': 'pollution_valankulam_2024',
            'lake_name': 'Valankulam',
            'alert_type': 'pollution_source',
            'severity': 'high',
            'message': 'New pollution source detected in northeast catchment area',
            'timestamp': '2024-11-15T16:20:00Z',
            'recommended_action': 'Investigate industrial discharge and implement immediate containment'
        }
    ]
    
    return jsonify({
        'alerts': alerts,
        'total_alerts': len(alerts),
        'last_updated': '2024-11-25T12:00:00Z'
    })

@app.route('/api/pollution-sources/<lake_id>', methods=['GET'])
def get_pollution_sources(lake_id):
    """Get detailed pollution source mapping for a specific lake"""
    try:
        # Check if Earth Engine is available
        try:
            ee.Number(1).getInfo()
            return get_real_pollution_sources(lake_id)
        except:
            return get_mock_pollution_sources(lake_id)
    except Exception as e:
        print(f"Error in get_pollution_sources: {str(e)}")
        return get_mock_pollution_sources(lake_id)

def get_real_pollution_sources(lake_id):
    """Get real pollution sources using Earth Engine land use analysis"""
    try:
        lakes = load_lakes_from_files()
        
        lake_name = lake_id.replace('_', ' ').title()
        matching_lakes = [name for name in lakes.keys() if lake_name.lower() in name.lower()]
        
        if not matching_lakes:
            return jsonify({'error': 'Lake not found'}), 404
        
        lake_name = matching_lakes[0]
        lake_fc = lakes[lake_name]
        
        # Create buffer around lake for catchment analysis
        catchment = lake_fc.geometry().buffer(2000)  # 2km buffer
        
        # Get land use data (using Sentinel-2 for basic classification)
        s2 = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterDate('2023-01-01', '2024-12-31') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
            .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']) \
            .median()
        
        # Simple land use classification
        ndvi = s2.normalizedDifference(['B8', 'B4'])
        ndbi = s2.normalizedDifference(['B11', 'B8'])
        mndwi = s2.normalizedDifference(['B3', 'B11'])
        
        # Classify land use
        urban = ndbi.gt(0.1).And(ndvi.lt(0.2))
        industrial = ndbi.gt(0.2).And(ndvi.lt(0.1))
        water = mndwi.gt(0.3)
        vegetation = ndvi.gt(0.4)
        
        # Calculate areas
        urban_area = urban.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=catchment,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        industrial_area = industrial.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=catchment,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        water_area = water.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=catchment,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        vegetation_area = vegetation.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=catchment,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        total_area = catchment.area().getInfo()
        
        # Calculate pollution risk scores
        urban_percent = (urban_area.get('nd', 0) / total_area) * 100
        industrial_percent = (industrial_area.get('nd', 0) / total_area) * 100
        
        pollution_risk = min(100, (urban_percent * 0.6) + (industrial_percent * 1.5))
        
        return jsonify({
            'lake_name': lake_name,
            'catchment_analysis': {
                'total_area_km2': round(total_area / 1000000, 2),
                'urban_coverage_percent': round(urban_percent, 1),
                'industrial_coverage_percent': round(industrial_percent, 1),
                'vegetation_coverage_percent': round((vegetation_area.get('nd', 0) / total_area) * 100, 1),
                'water_coverage_percent': round((water_area.get('nd', 0) / total_area) * 100, 1)
            },
            'pollution_risk_score': round(pollution_risk, 1),
            'risk_level': 'High' if pollution_risk > 70 else 'Medium' if pollution_risk > 40 else 'Low',
            'identified_sources': get_identified_sources(lake_id, pollution_risk),
            'recommendations': get_pollution_recommendations(pollution_risk, urban_percent, industrial_percent)
        })
        
    except Exception as e:
        print(f"Error in get_real_pollution_sources: {str(e)}")
        return get_mock_pollution_sources(lake_id)

def get_mock_pollution_sources(lake_id):
    """Generate mock pollution source mapping data"""
    
    pollution_data = {
        'ukkadam': {
            'risk_score': 85,
            'urban_percent': 45,
            'industrial_percent': 25,
            'sources': [
                {'type': 'Industrial Discharge', 'severity': 'High', 'distance_km': 0.8},
                {'type': 'Urban Runoff', 'severity': 'High', 'distance_km': 0.3},
                {'type': 'Sewage Treatment Plant', 'severity': 'Medium', 'distance_km': 1.2}
            ]
        },
        'valankulam': {
            'risk_score': 65,
            'urban_percent': 35,
            'industrial_percent': 15,
            'sources': [
                {'type': 'Agricultural Runoff', 'severity': 'Medium', 'distance_km': 1.5},
                {'type': 'Urban Runoff', 'severity': 'Medium', 'distance_km': 0.6},
                {'type': 'Construction Activities', 'severity': 'Low', 'distance_km': 2.1}
            ]
        },
        'kurichi': {
            'risk_score': 45,
            'urban_percent': 25,
            'industrial_percent': 8,
            'sources': [
                {'type': 'Residential Wastewater', 'severity': 'Medium', 'distance_km': 0.9},
                {'type': 'Road Runoff', 'severity': 'Low', 'distance_km': 0.4}
            ]
        },
        'perur': {
            'risk_score': 75,
            'urban_percent': 40,
            'industrial_percent': 20,
            'sources': [
                {'type': 'Textile Industry', 'severity': 'High', 'distance_km': 1.1},
                {'type': 'Urban Runoff', 'severity': 'Medium', 'distance_km': 0.5},
                {'type': 'Market Waste', 'severity': 'Medium', 'distance_km': 0.7}
            ]
        },
        'singanallur': {
            'risk_score': 55,
            'urban_percent': 30,
            'industrial_percent': 12,
            'sources': [
                {'type': 'Urban Runoff', 'severity': 'Medium', 'distance_km': 0.4},
                {'type': 'Small Industries', 'severity': 'Medium', 'distance_km': 1.3},
                {'type': 'Agricultural Runoff', 'severity': 'Low', 'distance_km': 2.0}
            ]
        }
    }
    
    lake_data = pollution_data.get(lake_id, pollution_data['ukkadam'])
    
    return jsonify({
        'lake_name': lake_id.replace('_', ' ').title(),
        'catchment_analysis': {
            'total_area_km2': 12.5,
            'urban_coverage_percent': lake_data['urban_percent'],
            'industrial_coverage_percent': lake_data['industrial_percent'],
            'vegetation_coverage_percent': max(0, 100 - lake_data['urban_percent'] - lake_data['industrial_percent'] - 10),
            'water_coverage_percent': 10
        },
        'pollution_risk_score': lake_data['risk_score'],
        'risk_level': 'High' if lake_data['risk_score'] > 70 else 'Medium' if lake_data['risk_score'] > 40 else 'Low',
        'identified_sources': lake_data['sources'],
        'recommendations': get_pollution_recommendations(
            lake_data['risk_score'], 
            lake_data['urban_percent'], 
            lake_data['industrial_percent']
        )
    })

def get_identified_sources(lake_id, pollution_risk):
    """Generate identified pollution sources based on analysis"""
    sources = []
    
    if pollution_risk > 70:
        sources.extend([
            {'type': 'Industrial Discharge', 'severity': 'High', 'distance_km': 1.2},
            {'type': 'Urban Runoff', 'severity': 'High', 'distance_km': 0.5}
        ])
    elif pollution_risk > 40:
        sources.extend([
            {'type': 'Urban Runoff', 'severity': 'Medium', 'distance_km': 0.8},
            {'type': 'Agricultural Runoff', 'severity': 'Medium', 'distance_km': 1.5}
        ])
    else:
        sources.append({'type': 'Natural Runoff', 'severity': 'Low', 'distance_km': 2.0})
    
    return sources

def get_pollution_recommendations(risk_score, urban_percent, industrial_percent):
    """Generate recommendations based on pollution analysis"""
    recommendations = []
    
    if risk_score > 70:
        recommendations.extend([
            "Immediate enforcement of industrial discharge regulations",
            "Install real-time water quality monitoring systems",
            "Implement emergency pollution response protocols"
        ])
    
    if urban_percent > 30:
        recommendations.append("Improve urban stormwater management and sewage treatment")
    
    if industrial_percent > 15:
        recommendations.append("Conduct detailed industrial effluent audits and implement stricter controls")
    
    recommendations.extend([
        "Establish buffer zones with native vegetation around the lake",
        "Regular community awareness programs on water conservation",
        "Quarterly water quality assessments and public reporting"
    ])
    
    return recommendations

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
