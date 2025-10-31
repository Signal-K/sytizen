# Supabase Upload Scripts

This directory contains Python scripts for uploading files and creating anomaly records in Supabase.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Create a `.env` file in this directory:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Supabase credentials:
   - Get your cloud credentials from: https://app.supabase.com/project/_/settings/api
   - Copy the `URL`, `service_role_key`, and `anon_key`
   - Paste them into the corresponding variables in `.env`

## Environment Variables

The scripts use the following environment variables:

### Cloud Supabase (Production)
- `SUPABASE_CLOUD_URL` - Your Supabase project URL
- `SUPABASE_CLOUD_SERVICE_ROLE_KEY` - Service role key (required for storage uploads)
- `SUPABASE_CLOUD_ANON_KEY` - Anonymous key (fallback)

### Local Supabase (Development)
- `SUPABASE_LOCAL_URL` - Local Supabase URL (default: http://127.0.0.1:54321)
- `SUPABASE_LOCAL_SERVICE_ROLE_KEY` - Local service role key
- `SUPABASE_LOCAL_ANON_KEY` - Local anonymous key

## Available Scripts

### `upload_ngts.py`
Uploads NGTS telescope images to both cloud and local Supabase instances.
```bash
python3 upload_ngts.py [directory]
```

### `upload_sunspots.py`
Uploads sunspot images to both cloud and local Supabase instances.
```bash
python3 upload_sunspots.py [directory]
```

### `upload.py`
General upload script for various anomaly types.
```bash
python3 upload.py
```

### `upload_bumble.py`
Uploads bumble images.
```bash
python3 upload_bumble.py
```

### `uploadForDir.py`
Uploads files organized in subdirectories (e.g., Mars cloud shapes).
```bash
python3 uploadForDir.py
```

### `uploadForce.py`
Force uploads files, overwriting existing ones.
```bash
python3 uploadForce.py
```

## Security Notes

- **Never commit your `.env` file to Git!** It's already in `.gitignore`.
- The `.env.example` file shows the structure but contains placeholder values.
- Service role keys have elevated permissions - keep them secure.
- Local Supabase keys are safe to commit as they're only for local development.

## Usage Examples

```bash
# Upload NGTS telescope images
python3 upload_ngts.py telescope/telescope-ngts

# Upload sunspot images (auto-detects directory)
python3 upload_sunspots.py

# Upload bumble images
python3 upload_bumble.py
```
