import noise
import numpy as np
from PIL import Image

# Define the size of the planet texture
texture_size = 1024

# Define the parameters for generating the planet
planet_radius = 1.0  # If > 2, planet would be a gas giant. Convert this from the radius parameter in planetsss
land_threshold = 0.1 # How much land is generated.
water_level = 0.001  # Water level on the planet
life_toggle = True  # Toggle for life presence
gas_giant_toggle = False
if planet_radius >= 2.0:
    gas_giant_toggle = True
rings_toggle = False  # False by default

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

            # Shift the moisture values to be positive
            moisture_map[i][j] = (moisture_map[i][j] + 1) / 2

    return moisture_map

# Generate the planet texture based on the height and moisture maps
def generate_planet_texture(height_map, moisture_map):
    texture = Image.new("RGB", (texture_size, texture_size))
    pixels = texture.load()

    # Define biome colors
    ocean_color = (0, 51, 102) # Dark blue for ocean
    beach_color = (255, 255, 204) # Cream color for beach
    mesa_color = (204, 85, 0) # Reddish-orange color for mesa
    desert_color = (255, 153, 51) # Yellowish-orange color for desert
    savannah_color = (153, 204, 0) # Faded dark green for savannah

    for i in range(texture_size):
        for j in range(texture_size):
            height = height_map[i % height_map.shape[0]][j % height_map.shape[1]]
            moisture = moisture_map[i % moisture_map.shape[0]][j % moisture_map.shape[1]]

            # Apply ocean color
            if height <= water_level:
                color = ocean_color
            # Apply beach color
            elif height <= land_threshold and height > water_level:
                color = beach_color
            # Apply mesa color
            elif height <= land_threshold + 0.1 and height > land_threshold:
                color = mesa_color
            # Apply desert color
            elif height <= land_threshold + 0.2 and height > land_threshold + 0.1:
                color = desert_color
            # Apply savannah color
            elif height > land_threshold + 0.2:
                color = savannah_color

            pixels[i, j] = color

    return texture

# Generate the planet snapshot
def generate_planet_snapshot():
    # Generate height and moisture maps
    height_map = generate_height_map(texture_size, scale=100)
    moisture_map = generate_moisture_map(texture_size, scale=200)

    # Generate planet texture
    planet_texture = generate_planet_texture(height_map, moisture_map)

    # Save the texture to a file (optional)
    planet_texture.save("output/planet_snapshot.png")

    return planet_texture

# Generate the planet topology
def generate_planet_topology():
    # Generate height map
    height_map = generate_height_map(texture_size, scale=100)

    # Normalize the height map for visualization
    normalized_height_map = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))

    # Create a colored image from the height map
    topology_image = Image.fromarray((normalized_height_map * 255).astype(np.uint8), mode='RGB')

    # Resize the image to a postcard-like size
    postcard_size = (600, 400)
    topology_image = topology_image.resize(postcard_size)

    # Save the image to a file (optional)
    topology_image.save("output/planet_topology.png")

    return topology_image

# Generate a sample planet snapshot
planet_snapshot = generate_planet_snapshot()
planet_snapshot.show()

# Generate a sample planet topology image
planet_topology = generate_planet_topology()
planet_topology.show()