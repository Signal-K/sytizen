import mongoengine as db
from pymongo import MongoClient

database_name = "planetData"
password = "7eyKlkQ48nYwA80w"
DB_URI = "mongodb+srv://Mongo:Ii2V1vkMsq58o9YB@cluster0.lzuxpat.mongodb.net/?retryWrites=true&w=majority" # Move back to below function later, currently this is sending to an empty/test table
"""DB_URI = "mongodb+srv://G1zmotronn:{}@cluster0.lzuxpat.mongodb.net/{}>retryWrites=true&w=majority".format(
    password, database_name
) # connection string to mongodb"""
db.connect(host=DB_URI)

# Collection class
class Planet(db.Document):
    planet_id = db.IntField()
    name = db.StringField()
    moonNumber = db.IntField()

    # Show JSON Output
    def to_json(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "moonNumber": self.moonNumber,
        }

# Create a new planet process
print("\nCreate a Planet")
planet = Planet(planet_id=1,
name = "Earth",
moonNumber = 1
)
planet.save() # Commit an item to MongoDB

# Fetching existing data
print("\nFetch a planet")
planet = Planet.objects(planet_id=1).first() # Return a single document that matches the query
print(planet.to_json())

# Update a planet/data
print("\n Update a planet")
planet.update(name="Mars",
moonNumber = 2)
print(planet.to_json())

# Add another planet
print("\nAdd another planet")
planet = Planet(planet_id=2,
name="Earth",
moonNumber = 1
)
planet.save()

# Fetch all planets from the database
print("\n Fetch all planets")
planets = [] # list
for planet in Planet.objects():
    planets.append(planet.to_json())
print(planets)

# Fetch planets from a query
print("\nFind planets whose name contains 'm'")
planets = []
for planet in Planet.objects(name__contains='m'):
    planets.append(planet.to_json())
print(planets)

# Query how many planets are in the collection
print("\nHow many planets are in this db?")
print(Planet.objects.count())

# Order the planets by planet name (alphabetical order)
print("\nOrder by planet name")
planets = []
for planet in Planet.objects().order_by('name'):
    planets.append(planet.to_json())
print(planets)

# Process to delete a planet by ID from the db
print("\nDelete a planet")
planet = Planet.objects(planet_id=2).first()
planet.delete()
print(Planet.objects.count())

# Delete all planets in the collection
print("\nDelete all the planets in this collection")
for planet in Planet.objects():
    planet.delete()
print(Planet.objects.count())

# mongo username: G1zmotronn
# mongo pw: 7eyKlkQ48nYwA80w // Ii2V1vkMsq58o9YB