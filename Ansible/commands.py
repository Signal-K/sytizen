python make_catalog.py --input sector-1-earlylook.csv sector-2-bright.csv sector-3-01.csv sector-3-02.csv --num_worker_processes=20 --base_dir=[wherever your csv file is] --out_name=tces.csv

# The original Astronet used Bazel, but we could just invoke the source scripts with the 
# following addition to PYTHONPATH:
export PYTHONPATH="/path/to/source/dir/:${PYTHONPATH}"

# Filename containing the CSV file of TCEs in the training set.
TCE_CSV_FILE="astronet/tces.csv"

# Directory to save output TFRecord files into.
TFRECORD_DIR="astronet/tfrecord"

# Directory where light curves are located.
TESS_DATA_DIR="astronet/tess/"
  
# Run without bazel
python astronet/data/generate_input_records.py \
--input_tce_csv_file=${TCE_CSV_FILE} \
--tess_data_dir=${TESS_DATA_DIR} \
--output_dir=${TFRECORD_DIR} \
--num_worker_processes=5 