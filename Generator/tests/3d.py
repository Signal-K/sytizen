import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
pygame.display.set_caption("3D Planet")

# Set up OpenGL perspective
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the planet
    glPushMatrix()
    glRotatef(1, 0, 1, 0)  # Rotate the planet around the y-axis
    glColor3f(0.3, 0.5, 1.0)  # Set the planet color
    gluSphere(gluNewQuadric(), 1, 32, 32)  # Render a sphere representing the planet
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

# Clean up resources
pygame.quit()

"""import noise
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
                color = (255, 255, 200)  # Cream, white, or yellow color
            # Apply transition color between land and water
            else:
                blend_factor = (height - water_level) / (land_threshold - water_level)
                color = (
                    int(255 * moisture * blend_factor),
                    int(255 * moisture * blend_factor),
                    int(255 * moisture * blend_factor),
                )

            pixels[i, j] = color

    return texture

# Generate the planet
def generate_planet():
    # Generate height and moisture maps
    height_map = generate_height_map(texture_size, scale=100)
    moisture_map = generate_moisture_map(texture_size, scale=200)

    # Generate planet texture
    planet_texture = generate_planet_texture(height_map, moisture_map)

    # Create a sphere mesh with UV mapping
    mesh = bpy.data.meshes.new("PlanetMesh")
    vertices = []
    edges = []
    faces = []
    for i in range(texture_size):
        for j in range(texture_size):
            x = i / texture_size * 2 - 1
            y = j / texture_size * 2 - 1
            z = height_map[i][j]
            vertices.append((x, y, z))
            if i < texture_size - 1 and j < texture_size - 1:
                v1 = i * texture_size + j
                v2 = i * texture_size + (j + 1)
                v3 = (i + 1) * texture_size + j
                v4 = (i + 1) * texture_size + (j + 1)
                faces.extend([(v1, v2, v4), (v1, v4, v3)])
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    # Create a material and assign the texture
    material = bpy.data.materials.new("PlanetMaterial")
    material.use_nodes = True
    material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Create texture node
    tex_node = nodes.new("ShaderNodeTexImage")
    tex_node.image = bpy.data.images.load("planet_texture.png")
    tex_node.location = (-400, 200)

    # Create diffuse shader node
    diffuse_node = nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node.location = (0, 200)

    # Create output node
    output_node = nodes.new("ShaderNodeOutputMaterial")
    output_node.location = (400, 200)

    # Connect the nodes
    links.new(tex_node.outputs["Color"], diffuse_node.inputs["Color"])
    links.new(diffuse_node.outputs["BSDF"], output_node.inputs["Surface"])

    # Assign the material to the mesh
    mesh_obj = bpy.data.objects.new("Planet", mesh)
    bpy.context.collection.objects.link(mesh_obj)
    mesh_obj.data.materials.append(material)

# Generate a sample planet
generate_planet()"""