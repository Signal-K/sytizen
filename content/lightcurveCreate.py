import os
import lightkurve as lk

def read_planet_anomalies(filename='anomalies_grouped.txt'):
    planet_anomalies = []
    found_planets = False

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("Anomalies of Type: planet"):
                found_planets = True
                continue
            if found_planets and line.strip():
                # Extract the ID from the line
                parts = line.split(',')
                if parts:
                    id_part = parts[0].strip()
                    if id_part.startswith('- ID:'):
                        planet_id = id_part.split(' ')[-1]
                        planet_anomalies.append(planet_id)
            if not line.strip() and found_planets:
                break  # Stop reading after the last entry for planets

    return planet_anomalies

def search_lightcurves_and_export(planet_anomalies, output_filename='lightcurve_results.txt'):
    with open(output_filename, 'w') as outfile:
        for planet_id in planet_anomalies:
            TIC_id = f'TIC {planet_id}'
            try:
                # Search for the light curve
                available_data_all = lk.search_lightcurve(TIC_id)
                
                # Check if any data is found
                if available_data_all:
                    outfile.write(f"{TIC_id} found:\n")
                    for lc in available_data_all:
                        outfile.write(f"  - {lc}\n")
                else:
                    outfile.write(f"{TIC_id} not found.\n")
            except Exception as e:
                outfile.write(f"Error searching {TIC_id}: {str(e)}\n")

        print(f"Lightcurve data exported to {output_filename}")

def main():
    planet_anomalies = read_planet_anomalies()
    search_lightcurves_and_export(planet_anomalies)

if __name__ == "__main__":
    main()
