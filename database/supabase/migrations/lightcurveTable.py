import supabase

supabase_url = 'https://your-supabase-url.com'
supabase_key = 'your-supabase-key'

client = supabase.Client(supabase_url, supabase_key)

# Create a new "planets" table
query = '''
CREATE TABLE planets (
  planetId UUID PRIMARY KEY,
  image TEXT,
  name TEXT,
  radius REAL,
  orbital_period REAL
);
'''
response = client.query(query)

print(response)