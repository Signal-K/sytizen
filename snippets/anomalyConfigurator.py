import numpy as np
from math import cos, pi, sqrt
from collections import defaultdict

def calculate_completion(params):
    required_params = ['confirmed', 'size', 'star_temp', 'distance', 'period', 'radius', 'mass', 'cloud_height', 'spectroscopy']
    provided_params = sum(1 for param in required_params if param in params and params[param] is not None)
    completion_percentage = (provided_params / len(required_params)) * 100
    return completion_percentage

def determine_planet_type(params):
    if 'size' in params and params['size'] is not None:
        if params['size'] <= 2:
            return "Terrestrial"
        elif params['size'] == 3:
            if 'distance' in params and params['distance'] is not None and params['distance'] < 1.5:
                return "Water world"
            return "Super-Earth"
        elif params['size'] <= 4:
            return "Ice giant"
        else:
            return "Gas Giant"
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
    elif planet_type == "Ice giant":
        color_map = ['#5bc0de', '#31b0d5', '#269abc', '#204d74']
    elif planet_type == "Gas Giant":
        color_map = ['#f0ad4e', '#ec971f', '#d58512', '#c67605']
    else:
        color_map = ['#5e5e5e', '#4e4e4e', '#3e3e3e', '#2e2e2e']

    # Adjust colors based on specific spectroscopy elements if provided
    return color_map

def generate_planet_image(params):
    """Generate the planet image based on provided parameters."""
    # Calculate temperature range
    temp_eq, temp_non_eq = calculate_temperature(params.get('star_temp', 5778), params.get('distance'), params.get('period'))
    
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
params = {
    'confirmed': True,
    'size': 3,
    'star_temp': 5778,
    'distance': 1.0,  # AU
    'period': None,
    'radius': 1.0,  # Earth radii
    'mass': 1.0,  # Earth masses
    'cloud_height': 0.5,
    'spectroscopy': ['water', 'iron']
}

planet_info = generate_planet_image(params)
print("Color Map:", planet_info["color_map"])
print("Planet Type:", planet_info["planet_type"])
print("Completion Percentage:", planet_info["completion_percentage"])
