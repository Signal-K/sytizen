import os
from supabase import create_client

url = os.getenv("SUPABASE_URL") # from your `.env` file
key = os.getenv("SUPABASE_KEY")
# supabase = create_client(url, key)
res = supabase.storage().from_('images').list()
data = supabase.table('todos').select('*').execute()
print(data)