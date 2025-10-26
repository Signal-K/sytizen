# NGTS (Next-Generation Transit Survey) Data Upload

This script uploads NGTS anomaly images and creates corresponding database entries in both local and cloud Supabase instances.

## About NGTS

The Next-Generation Transit Survey (NGTS) is based at the European Southern Observatory (ESO) Paranal Observatory in Chile. It consists of an array of twelve robotic telescopes designed to make high-precision measurements of exoplanet transits.

## Prerequisites

1. **Python Dependencies**:
   ```bash
   pip install supabase
   ```

2. **Directory Structure**:
   Create a directory at `citizen/buckets/telescope/telescope-ngts/` and place your NGTS image files there. Image filenames should be numeric IDs (e.g., `160075684.png`).

3. **Supabase Instances**:
   - Local Supabase should be running at `http://127.0.0.1:54321`
   - Cloud Supabase credentials are embedded in the script

## Usage

```bash
cd citizen/buckets
python upload_ngts.py
```

## What the Script Does

1. **Connects to Both Instances**:
   - Cloud Supabase: `https://hlufptwhzkpkkjztimzo.supabase.co`
   - Local Supabase: `http://127.0.0.1:54321`

2. **Uploads Images**:
   - Uploads each image to the `telescope/telescope-ngts` storage bucket
   - Uses the filename (without extension) as the anomaly ID

3. **Creates Database Entries**:
   - Inserts anomaly records with `anomalySet = "telescope-ngts"`
   - Structure matches TESS planet format:
     ```json
     {
       "id": 160075684,
       "content": "160075684",
       "anomalytype": "planet",
       "avatar_url": "telescope/telescope-ngts/160075684.png",
       "anomalySet": "telescope-ngts"
     }
     ```

4. **Updates Both Instances**:
   - All operations are performed on both local and cloud Supabase
   - Provides separate logging for each instance

## Features

- **Dual Upload**: Uploads to both local and cloud simultaneously
- **Error Handling**: Continues on failure, reports at the end
- **Upsert Logic**: Updates existing records instead of failing
- **Graceful Exit**: Ctrl+C exits cleanly
- **Progress Tracking**: Shows detailed upload status

## Unlocking NGTS Data in Game

Users can unlock NGTS data access by:
1. Completing 4+ planet classifications
2. Researching "Planet Hunters: Next Generation" for 2 stardust
3. Tech type stored as `ngtsAccess` in the `researched` table

Once unlocked, NGTS anomalies will appear when deploying the telescope in "Planetary Objects" mode.

## Troubleshooting

### Connection Issues
- Ensure local Supabase is running: `docker ps`
- Check network connectivity to cloud Supabase

### Upload Failures
- Verify bucket `telescope/telescope-ngts` exists in storage
- Check file permissions on image directory
- Ensure service role keys have storage permissions

### Database Errors
- Verify anomaly ID is unique
- Check that anomaly ID is a valid integer
- Ensure `anomalies` table schema matches expected structure

## File Structure

```
citizen/buckets/
├── upload_ngts.py          # This script
└── telescope/
    └── telescope-ngts/     # Place NGTS images here
        ├── 160075684.png
        ├── 160075685.png
        └── ...
```

## Output Example

```
============================================================
  NGTS Anomaly Upload Script
  Uploads to both LOCAL and CLOUD Supabase instances
============================================================

✓ Connected to cloud Supabase
✓ Connected to local Supabase

Configuration:
  Bucket: telescope/telescope-ngts
  Local Directory: telescope/telescope-ngts
  Anomaly Set: telescope-ngts

Processing: 160075684.png (ID: 160075684)
  [CLOUD] Uploaded telescope/telescope-ngts/160075684.png
  [CLOUD] Inserted anomaly 160075684 into anomalies table
  [LOCAL] Uploaded telescope/telescope-ngts/160075684.png
  [LOCAL] Inserted anomaly 160075684 into anomalies table

============================================================
Upload Summary:
  Files processed: 1
  Files failed: 0
============================================================

✓ Upload completed successfully!
```
