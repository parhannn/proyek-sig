from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from shapely import wkb
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class MapPoint(db.Model):
    __tablename__ = 'point_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    geom = db.Column(db.String)
    
class LineData(db.Model):
    __tablename__ = 'line_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    geom = db.Column(db.String)

class PolygonData(db.Model):
    __tablename__ = 'polygon_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    geom = db.Column(db.String)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map')
def map():
    geo_points = MapPoint.query.all()
    geo_lines = LineData.query.all()
    geo_polygons = PolygonData.query.all()

    geojson_features_points = []
    geojson_features_lines = []
    geojson_features_polygons = []

    for point in geo_points:
        if point.geom:  
            geom = wkb.loads(bytes.fromhex(point.geom))  
            longitude, latitude = geom.x, geom.y
            geojson_features_points.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                'properties': {
                    'name': point.name
                }
            })

    for line in geo_lines:
        if line.geom:
            geom = wkb.loads(bytes.fromhex(line.geom))
            coordinates = [list(coord) for coord in geom.coords]
            geojson_features_lines.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                },
                'properties': {
                    'name': line.name
                }
            })

    for polygon in geo_polygons:
        if polygon.geom:
            geom = wkb.loads(bytes.fromhex(polygon.geom))
            coordinates = [list(geom.exterior.coords)]
            geojson_features_polygons.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': coordinates
                },
                'properties': {
                    'name': polygon.name
                }
            })

    return render_template(
        'map.html', 
        geo_points=geojson_features_points if geojson_features_points else [],
        geo_lines=geojson_features_lines if geojson_features_lines else [],
        geo_polygons=geojson_features_polygons if geojson_features_polygons else []
    )

if __name__ == '__main__':
    app.run(debug=True)