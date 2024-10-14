OUTPUT_FILE="lightcurve_results.txt"
GROUPED_OUTPUT_FILE="grouped_sectors.txt"

# Check if the output file exists
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Output file $OUTPUT_FILE not found."
    exit 1
fi

# Extract unique sectors and format the output
echo "Extracting unique sectors and formatting output..."
{
    # Initialize variables
    current_tic=""
    first_sector=""

    # Read the output file line by line
    while IFS= read -r line; do
        # Check for a TIC ID line
        if [[ $line == TIC* ]]; then
            # If we have a current TIC, print the sectors for it only if we found a sector
            if [ -n "$current_tic" ] && [ -n "$first_sector" ]; then
                echo "TIC $current_tic: $first_sector" >> "$GROUPED_OUTPUT_FILE"
            fi
            
            # Reset variables and update current TIC
            current_tic=$(echo "$line" | cut -d ' ' -f 2)
            first_sector=""  # Reset the first sector for the new TIC
        fi
        
        # Check for sector lines and extract the first sector
        if [[ $line == *"TESS Sector"* ]]; then
            sector=$(echo "$line" | awk '{print $2, $3, $4}')  # Extract relevant columns
            # If first_sector is not set, set it to the current sector
            if [ -z "$first_sector" ]; then
                first_sector="$sector"
            fi
        fi
    done < "$OUTPUT_FILE"

    # Print the last TIC if it exists and has a sector
    if [ -n "$current_tic" ] && [ -n "$first_sector" ]; then
        echo "TIC $current_tic: $first_sector" >> "$GROUPED_OUTPUT_FILE"
    fi
}

echo "Unique sectors extracted and formatted in $GROUPED_OUTPUT_FILE."