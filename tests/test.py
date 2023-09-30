from astroquery.mast import Catalogs

def get_stellar_parameters(tic_id):
    try:
        # Query the MAST catalog for stellar parameters
        result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)

        if result is not None:
            # Extract relevant stellar parameters from the result
            star_name = result['TICID'][0]
            radius = result['rad'][0]  # Stellar radius
            metallicity = result['met'][0]  # Metallicity
            mass = result['mass'][0]  # Stellar mass
            density = result['rho'][0]  # Stellar density
            luminosity = result['lum'][0]  # Luminosity

            # Return the extracted data
            stellar_data = {
                "star_name": star_name,
                "radius": radius,
                "metallicity": metallicity,
                "mass": mass,
                "density": density,
                "luminosity": luminosity
            }
            return stellar_data
        else:
            return {"error": "Star not found in the MAST catalog"}
    except Exception as e:
        return {"error": str(e)}

# Example usage
tic_id = "55525572"
stellar_info = get_stellar_parameters(tic_id)
print(stellar_info)