import csv
import json
from math import cos, pi, sqrt
from collections import defaultdict

def calculate_completion(params):
    required_params = ['radius', 'mass', 'density', 'gravity', 'temperature_eq', 'temperature', 'smaxis', 'orbital_period']
    provided_params = sum(1 for param in required_params if param in params and params[param] is not None)
    completion_percentage = (provided_params / len(required_params)) * 100
    return completion_percentage

def determine_planet_type(params):
    if 'radius' in params and params['radius'] is not None:
        if params['radius'] <= 1.5:
            return "Terrestrial"
        elif params['radius'] <= 2.5:
            if 'temperature' in params and params['temperature'] is not None and params['temperature'] < 273:
                return "Icey terrestrial"
            if 'smaxis' in params and params['smaxis'] is not None and params['smaxis'] < 1.5:
                return "Water world"
            return "Super-Earth"
        elif params['radius'] <= 4:
            return "IceGiant"
        else:
            return "GasGiant"
    return "Anomaly"

def calculate_temperature(star_temp, distance=None, period=None):
    """Calculate equilibrium and non-equilibrium temperature range."""
    if distance is not None:
        temp_eq = (star_temp * (1 - 0.3)**0.25) / sqrt(2 * distance)
    elif period is not None:
        temp_eq = (star_temp * (1 - 0.3)**0.25) / sqrt(2 * (period / (2 * pi))**(2/3))
    else:
        temp_eq = 0  # Default value if no information is provided
    temp_non_eq = temp_eq * 1.1  # Non-equilibrium temperature
    return temp_eq, temp_non_eq

def generate_color_map(temp_eq, planet_type):
    """Generate a color map based on temperature and planet type."""
    color_map = []
    if planet_type in ["Terrestrial", "Super-Earth"]:
        if temp_eq > 373:
            color_map = ['#d9534f', '#c9302c', '#ac2925', '#761c19']
        elif temp_eq < 273:
            color_map = ['#5bc0de', '#46b8da', '#31b0d5', '#269abc']
        else:
            color_map = ['#5cb85c', '#4cae4c', '#449d44', '#398439']
    elif planet_type == "Water world":
        color_map = ['#5bc0de', '#46b8da', '#31b0d5', '#269abc']
    elif planet_type == "IceGiant":
        color_map = ['#5bc0de', '#31b0d5', '#269abc', '#204d74']
    elif planet_type == "GasGiant":
        color_map = ['#f0ad4e', '#ec971f', '#d58512', '#c67605']
    else:
        color_map = ['#5e5e5e', '#4e4e4e', '#3e3e3e', '#2e2e2e']

    # Ensure the color map has exactly 8 colors
    while len(color_map) < 8:
        color_map.extend(color_map[:8 - len(color_map)])
    return color_map[:8]

def parse_configuration(config_str):
    config = json.loads(config_str)
    return {
        'mass': float(config.get('mass', 0)),
        'ticId': config.get('ticId'),
        'radius': float(config.get('radius', 0)),
        'smaxis': float(config.get('smaxis', 0)),
        'density': float(config.get('density', 0)),
        'gravity': float(config.get('gravity', 0)),
        'lightkurve': config.get('lightkurve'),
        'temperature': float(config.get('temperature', 0)),
        'orbital_period': float(config.get('orbital_period', 0)),
        'temperature_eq': float(config.get('temperature_eq', 0)),
    }

def generate_planet_image(params):
    """Generate the planet image based on provided parameters."""
    # Calculate temperature range
    temp_eq, temp_non_eq = calculate_temperature(5778, params.get('smaxis'), params.get('orbital_period'))
    
    # Determine planet type
    planet_type = determine_planet_type(params)
    
    # Generate color map
    color_map = generate_color_map(temp_eq, planet_type)
    
    # Calculate completion percentage
    completion_percentage = calculate_completion(params)
    
    return {
        "color_map": color_map,
        "planet_type": planet_type,
        "completion_percentage": completion_percentage
    }

# Example usage
csv_data = """id,content,ticId,anomalytype,type,radius,mass,density,gravity,temperatureEq,temperature,smaxis,orbital_period,classification_status,avatar_url,created_at,deepnote,lightkurve,configuration
1,Kepler-69c,,planet,Super-Earth,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base3.png,2023-12-09 22:45:53.406827+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/c0a1f3fb754c4d8e9a4af06561bdf63b?height=2137,,"{""mass"":2.14,""ticId"":""KOI 172.02"",""radius"":1.71,""smaxis"":0.64,""density"":2.36,""gravity"":0.73,""lightkurve"":""https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planetsss/_1710155300825"",""temperature"":325.15,""orbital_period"":242.47,""temperature_eq"":548.15}"
2,Kepler-186f,,planet,Terrestrial Earth-like,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base6.png,2023-12-11 02:14:32.494124+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/26fe61c341554e0eb36d116ea86cc371?height=1214.46875,,"{""mass"":1.44,""ticId"":""KOI 571.05"",""radius"":1.17,""smaxis"":0.432,""gravity"":1.17,""lightkurve"":""https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planetsss/_1710155300825"",""temperature"":-85,""orbital_period"":129.95}"
3,Kepler-442b,,planet,Terrestrial Super-Earth,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base2.png,2023-12-11 07:04:10.985628+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/cc87705e6f8741548f240421ad98eb8a?height=840.34375,,"{""mass"":2.3,""ticId"":""KOI-4742.01"",""radius"":1.34,""smaxis"":0.409,""lightkurve"":""https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planetsss/_1710159536497"",""orbital_period"":112.3,""temperature_eq"":233}"
4,Kepler-22b,,planet,Water world,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base6.png,2023-12-11 07:06:10.540091+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/de23ffaa2ccc4d0d8889cefbfbda83df?height=388.78125,,"{""mass"":9.1,""ticId"":""KOI-87.01"",""radius"":2.1,""smaxis"":0.812,""density"":5.2,""temperature"":295,""orbital_period"":289.86,""temperature_eq"":279}"
5,Trappist-1f,,planet,Terrestrial earth-size,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base1.png,2023-12-11 07:10:40.276653+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/2e256956eb414262ae3902216eeb924f?height=440,,"{""mass"":1.039,""ticId"":""TOI 6838.05"",""radius"":1.045,""smaxis"":0.03749,""density"":5.009,""orbital_period"":9.21,""temperature_eq"":217.65}"
6,TOI-700d,,planet,Goldilocks terrestrial earth-like,,,,,,,,,,https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/avatars/Base6.png,2023-12-11 07:12:23.761093+00,https://embed.deepnote.com/f8de697b-ba49-4014-b2b2-fe5f4cc3c026/da5fa6f8ac26477b841b89a02a690805/209424fcd5de426bbdd87d1e5420dde4?height=598.75,,"{""mass"":1.72,""ticId"":""TOI-700.02"",""radius"":1.073,""smaxis"":0.1633,""orbital_period"":37.42,""temperature_eq"":268.85}"""

def process_csv_data(csv_data):
    planets = []
    reader = csv.DictReader(csv_data.splitlines())
    for row in reader:
        planet_data = parse_configuration(row['configuration'])
        planet_data.update({
            'id': row['id'],
            'content': row['content'],
            'ticId': row['ticId'],
            'anomalytype': row['anomalytype'],
            'type': row['type'],
            'radius': float(row['radius']) if row['radius'] else None,
            'mass': float(row['mass']) if row['mass'] else None,
            'density': float(row['density']) if row['density'] else None,
            'gravity': float(row['gravity']) if row['gravity'] else None,
            'temperature_eq': float(row['temperatureEq']) if row['temperatureEq'] else None,
            'temperature': float(row['temperature']) if row['temperature'] else None,
            'smaxis': float(row['smaxis']) if row['smaxis'] else None,
            'orbital_period': float(row['orbital_period']) if row['orbital_period'] else None,
            'classification_status': row['classification_status'],
            'avatar_url': row['avatar_url'],
            'created_at': row['created_at'],
            'deepnote': row['deepnote'],
            'lightkurve': row['lightkurve']
        })
        planets.append(planet_data)
    return planets

planets = process_csv_data(csv_data)

for planet in planets:
    planet_info = generate_planet_image(planet)
    print(f"Planet {planet['content']} ({planet['id']}):")
    print("  Color Map:", planet_info["color_map"])
    print("  Planet Type:", planet_info["planet_type"])
    print("  Completion Percentage:", planet_info["completion_percentage"])