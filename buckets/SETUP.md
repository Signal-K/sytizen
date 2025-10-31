# Quick Start Guide for Supabase Upload Scripts

## Installation

1. **Navigate to the citizen directory:**
   ```bash
   cd /Users/scroobz/Navigation/client/citizen
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   # or
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cd buckets
   cp .env.example .env
   ```

4. **Edit the `.env` file with your credentials:**
   ```bash
   # Open in your favorite editor
   nano .env
   # or
   code .env
   ```

5. **Add your Supabase cloud credentials:**
   - Go to https://app.supabase.com/project/_/settings/api
   - Copy your project URL, service role key, and anon key
   - Paste them into the `.env` file

## Example `.env` file

```env
# Cloud Supabase (your production instance)
SUPABASE_CLOUD_URL=https://hlufptwhzkpkkjztimzo.supabase.co
SUPABASE_CLOUD_SERVICE_ROLE_KEY=eyJhbGc...your-actual-key-here
SUPABASE_CLOUD_ANON_KEY=eyJhbGc...your-actual-key-here

# Local Supabase (development - these defaults usually work)
SUPABASE_LOCAL_URL=http://127.0.0.1:54321
SUPABASE_LOCAL_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
SUPABASE_LOCAL_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

## Running Upload Scripts

```bash
# From the buckets directory
cd /Users/scroobz/Navigation/client/citizen/buckets

# Upload sunspots
python3 upload_sunspots.py

# Upload NGTS data
python3 upload_ngts.py

# Upload other data
python3 upload.py
```

## Security Reminders

- ✅ `.env` is in `.gitignore` - won't be committed
- ✅ `.env.example` has placeholders - safe to commit
- ⚠️ Never commit actual credentials to Git
- 🔒 Keep your service role key secure - it has elevated permissions

## Troubleshooting

### Import error for dotenv
If you see `Import "dotenv" could not be resolved`, install dependencies:
```bash
pip3 install python-dotenv
```

### Connection errors
- For cloud: Check your credentials in `.env`
- For local: Make sure Supabase is running locally (`supabase start`)

### Permission errors
- Make sure you're using the service role key, not the anon key
- Check your bucket permissions in Supabase dashboard
