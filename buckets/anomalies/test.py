from astroquery.mast import Catalogs

def fetch_tic_data(tic_id):
    """
    Fetches and prints all available data for a given TIC ID.

    Parameters:
    - tic_id: The TIC ID to query.
    """
    # Query the TIC catalog for the given TIC ID
    star_info = Catalogs.query_object(f"TIC {tic_id}", catalog="TIC")

    if len(star_info) == 0:
        print(f"No data found for TIC {tic_id}.")
        return

    # Retrieve the first matching entry
    star_data = star_info[0]

    # Print all column headers and their corresponding values
    for column in star_data.colnames:
        print(f"{column}: {star_data[column]}")

# Example usage
tic_id = 440801822  # Replace with your TIC ID
fetch_tic_data(tic_id)