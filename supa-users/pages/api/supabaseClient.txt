import { createClient } from "@supabase/supabase-js";
import Moralis from "moralis/.";

const NEXT_PUBLIC_SUPABASE_URL="https://afwwxlhknelxylrfvexi.supabase.co";
const NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo";


const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

const supabase = createClient(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY);
Moralis.start({
    apiKey: process.env.MORALIS_API_KEY,
});

export async function requestMessage({ address, chain, network }: { address: string; chain: string; network: 'evm' }) {
  const result = await Moralis.Auth.requestMessage({
    address,
    chain,
    network,
    domain: 'defi.finance',
    statement: 'Please sign this message to confirm your identity.',
    uri: 'https://defi.finance',
    expirationTime: '2023-01-01T00:00:00.000Z',
    timeout: 15,
  });
  
  const { message } = result.toJSON();

  return message;
};