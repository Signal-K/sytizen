from supabase import create_client, Client

url = "http://127.0.0.1:54321"  
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
supabase: Client = create_client(url, key)

# Predefined anomaly data
anomalies = [
    # {"content": "Mercury", "id": 10, "mass": "3.3011×10^23 kg", "gravity": "3.7 m/s²", "density": "5.427 g/cm³", "radius": "2439.7 km", "dominant_color": "Gray", "planet_type": "Terrestrial", "equilibrium_temp": "440 K", "semi_major_axis": "0.387 AU"},
    {"content": "Venus", "id": 20, "mass": "4.8675×10^24 kg", "gravity": "8.87 m/s²", "density": "5.243 g/cm³", "radius": "6051.8 km", "dominant_color": "Yellow", "planet_type": "Terrestrial", "equilibrium_temp": "737 K", "semi_major_axis": "0.723 AU"},
    # {"content": "Earth", "id": 69, "mass": "5.97237×10^24 kg", "gravity": "9.8 m/s²", "density": "5.514 g/cm³", "radius": "6371 km", "dominant_color": "Blue", "planet_type": "Terrestrial", "equilibrium_temp": "288 K", "semi_major_axis": "1.000 AU"},
    {"content": "Moon", "id": 31, "mass": "7.342×10^22 kg", "gravity": "1.62 m/s²", "density": "3.344 g/cm³", "radius": "1737.4 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "220 K", "semi_major_axis": "0.00257 AU"},
    # {"content": "Mars", "id": 40, "mass": "6.4171×10^23 kg", "gravity": "3.71 m/s²", "density": "3.9335 g/cm³", "radius": "3389.5 km", "dominant_color": "Red", "planet_type": "Terrestrial", "equilibrium_temp": "210 K", "semi_major_axis": "1.524 AU"},
    {"content": "Jupiter", "id": 50, "mass": "1.8982×10^27 kg", "gravity": "24.79 m/s²", "density": "1.326 g/cm³", "radius": "69911 km", "dominant_color": "Brown", "planet_type": "Gas giant", "equilibrium_temp": "165 K", "semi_major_axis": "5.204 AU"},
    {"content": "Saturn", "id": 60, "mass": "5.6834×10^26 kg", "gravity": "10.44 m/s²", "density": "0.687 g/cm³", "radius": "58232 km", "dominant_color": "Yellow", "planet_type": "Gas giant", "equilibrium_temp": "134 K", "semi_major_axis": "9.582 AU"},
    {"content": "Uranus", "id": 70, "mass": "8.6810×10^25 kg", "gravity": "8.69 m/s²", "density": "1.27 g/cm³", "radius": "25362 km", "dominant_color": "Cyan", "planet_type": "Ice giant", "equilibrium_temp": "76 K", "semi_major_axis": "19.218 AU"},
    {"content": "Neptune", "id": 80, "mass": "1.02413×10^26 kg", "gravity": "11.15 m/s²", "density": "1.638 g/cm³", "radius": "24622 km", "dominant_color": "Blue", "planet_type": "Ice giant", "equilibrium_temp": "72 K", "semi_major_axis": "30.07 AU"},
    {"content": "Pluto", "id": 90, "mass": "1.303×10^22 kg", "gravity": "0.62 m/s²", "density": "1.854 g/cm³", "radius": "1188.3 km", "dominant_color": "Brown", "planet_type": "Dwarf planet", "equilibrium_temp": "44 K", "semi_major_axis": "39.48 AU"},
    {"content": "Deimos", "id": 42, "mass": "1.476×10^15 kg", "gravity": "0.003 m/s²", "density": "1.471 g/cm³", "radius": "6.2 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "233 K", "semi_major_axis": "0.00016 AU"},
    {"content": "Phobos", "id": 41, "mass": "1.0659×10^16 kg", "gravity": "0.0057 m/s²", "density": "1.876 g/cm³", "radius": "11.3 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "233 K", "semi_major_axis": "0.00006 AU"},
    {"content": "Ceres", "id": 43, "mass": "9.3835×10^20 kg", "gravity": "0.27 m/s²", "density": "2.16 g/cm³", "radius": "473 km", "dominant_color": "Gray", "planet_type": "Dwarf planet", "equilibrium_temp": "167 K", "semi_major_axis": "2.767 AU"},
    {"content": "Amalthea", "id": 51, "mass": "2.08×10^18 kg", "gravity": "0.029 m/s²", "density": "0.86 g/cm³", "radius": "83.5 km", "dominant_color": "Red", "planet_type": "Natural satellite", "equilibrium_temp": "123 K", "semi_major_axis": "0.0026 AU"},
    {"content": "Io", "id": 52, "mass": "8.9319×10^22 kg", "gravity": "1.796 m/s²", "density": "3.528 g/cm³", "radius": "1821.6 km", "dominant_color": "Yellow", "planet_type": "Natural satellite", "equilibrium_temp": "110 K", "semi_major_axis": "0.0028 AU"},
    {"content": "Europa", "id": 55, "mass": "4.7998×10^22 kg", "gravity": "1.315 m/s²", "density": "3.013 g/cm³", "radius": "1560.8 km", "dominant_color": "White", "planet_type": "Natural satellite", "equilibrium_temp": "102 K", "semi_major_axis": "0.0045 AU"},
    {"content": "Callisto", "id": 53, "mass": "1.0759×10^23 kg", "gravity": "1.235 m/s²", "density": "1.834 g/cm³", "radius": "2410.3 km", "dominant_color": "Brown", "planet_type": "Natural satellite", "equilibrium_temp": "134 K", "semi_major_axis": "0.0126 AU"},
    {"content": "Ganymede", "id": 54, "mass": "1.4819×10^23 kg", "gravity": "1.428 m/s²", "density": "1.936 g/cm³", "radius": "2634.1 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "110 K", "semi_major_axis": "0.0072 AU"},
    {"content": "Titan", "id": 62, "mass": "1.3452×10^23 kg", "gravity": "1.352 m/s²", "density": "1.881 g/cm³", "radius": "2574.7 km", "dominant_color": "Orange", "planet_type": "Natural satellite", "equilibrium_temp": "94 K", "semi_major_axis": "0.0082 AU"},
    {"content": "Enceladus", "id": 63, "mass": "1.08×10^20 kg", "gravity": "0.113 m/s²", "density": "1.61 g/cm³", "radius": "252.1 km", "dominant_color": "White", "planet_type": "Natural satellite", "equilibrium_temp": "75 K", "semi_major_axis": "0.0041 AU"},
    {"content": "Miranda", "id": 71, "mass": "6.59×10^19 kg", "gravity": "0.079 m/s²", "density": "1.2 g/cm³", "radius": "235.8 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "60 K", "semi_major_axis": "0.0012 AU"},
    {"content": "Oberon", "id": 72, "mass": "3.014×10^21 kg", "gravity": "0.351 m/s²", "density": "1.63 g/cm³", "radius": "761.4 km", "dominant_color": "Gray", "planet_type": "Natural satellite", "equilibrium_temp": "75 K", "semi_major_axis": "0.002 AU"},
    {"content": "Triton", "id": 81, "mass": "2.14×10^22 kg", "gravity": "0.779 m/s²", "density": "2.061 g/cm³", "radius": "1353.4 km", "dominant_color": "Pink", "planet_type": "Natural satellite", "equilibrium_temp": "38 K", "semi_major_axis": "0.0024 AU"}
]

# Insert anomalies into the Supabase table
for anomaly in anomalies:
    configuration = {
        "mass": anomaly["mass"],
        "gravity": anomaly["gravity"],
        "density": anomaly["density"],
        "radius": anomaly["radius"],
        "dominant_colour": anomaly["dominant_color"],
        "planet_type": anomaly["planet_type"],
        "equilibrium_temperature": anomaly["equilibrium_temp"],
        "semi_major_axis": anomaly["semi_major_axis"]
    }
    data = {
        "id": anomaly["id"],
        "content": anomaly["content"],
        "anomalytype": "space-body",
        "anomalySet": "solar-system",
        "configuration": configuration
    }
    response = supabase.table('anomalies').insert(data).execute()
    print(f"Inserted {anomaly['content']}: {response.data}")