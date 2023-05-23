import noise
import numpy as np
from PIL import Image

# Define the size of the planet texture
texture_size = 1024

# Define the parameters for generating the planet
planet_radius = 1.0
land_threshold = 0.2
water_level = 0.2

# Generate the height map using Perlin noise
def generate_height_map(size, scale):
    shape = (size, size)
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0

    height_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            height_map[i][j] = noise.pnoise2(
                i / scale,
                j / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=size,
                repeaty=size,
                base=0,
            )
    return height_map

# Generate the moisture map using Perlin noise
def generate_moisture_map(size, scale):
    shape = (size, size)
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0

    moisture_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            moisture_map[i][j] = noise.pnoise2(
                i / scale,
                j / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=size,
                repeaty=size,
                base=0,
            )
    return moisture_map

# Generate the planet texture based on the height and moisture maps
def generate_planet_texture(height_map, moisture_map):
    texture = Image.new("RGB", (texture_size, texture_size))
    pixels = texture.load()

    for i in range(texture_size):
        for j in range(texture_size):
            height = height_map[i % height_map.shape[0]][j % height_map.shape[1]]
            moisture = moisture_map[i % moisture_map.shape[0]][j % moisture_map.shape[1]]

            # Apply land color
            if height > land_threshold:
                color = (int(255 * moisture), int(255 * moisture), int(255 * moisture))
            # Apply water color
            elif height < water_level:
                color = (0, 0, int(255 * moisture))
            # Apply transition color between land and water
            else:
                blend_factor = (height - water_level) / (land_threshold - water_level)
                color = (int(255 * moisture * blend_factor), int(255 * moisture * blend_factor), 0)

            pixels[i, j] = color

    return texture

# Generate the planet
def generate_planet():
    # Generate height and moisture maps
    height_map = generate_height_map(texture_size, scale=100)
    moisture_map = generate_moisture_map(texture_size, scale=200)

    # Generate planet texture
    planet_texture = generate_planet_texture(height_map, moisture_map)
    
    # Save the texture to a file (optional)
    planet_texture.save("planet_texture.png")

    return planet_texture

# Generate a sample planet
planet = generate_planet()
planet.show()