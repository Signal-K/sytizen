import csv
import lightkurve as lk
import matplotlib.pyplot as plt

# Function to generate lightcurves
def generate_lightcurve(TIC):
    TIC_str = f'TIC {TIC}'  # Formatting the TIC ID
    try:
        available_data_all = lk.search_lightcurve(TIC_str)
        sector_data = available_data_all.download()

        if sector_data:
            bin_time = 15 / 24 / 30
            lc_collection_binned = sector_data.bin(bin_time)

            # Create a figure and axis
            fig, ax = plt.subplots()

            # Set the axis face color to transparent
            ax.set_facecolor('none')
            fig.patch.set_alpha(0)

            # Plotting the binned lightcurve
            lc_collection_binned.plot(ax=ax, color='red', lw=0, marker='.')

            # Save the figure with a transparent background
            plt.savefig(f'{TIC}_lightcurve.png', transparent=True)
            plt.close()

            print(f"Lightcurve for TIC {TIC} saved successfully.")
        else:
            print(f"No data found for TIC {TIC}")
    except Exception as e:
        print(f"Error processing TIC {TIC}: {str(e)}")

# Reading CSV and extracting the first 10 TIC IDs
def process_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        tic_count = 0

        for row in reader:
            if tic_count >= 10:
                break

            TIC_ID = row['TICID']
            generate_lightcurve(TIC_ID)

            tic_count += 1

# Run the script
if __name__ == '__main__':
    csv_filename = 'exofop.csv'
    process_csv(csv_filename)