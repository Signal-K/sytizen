import { useEffect, useState } from 'react';
import { supabase } from './initSupabase';
import Login from './supabaseLogin';
import Profile from './supabaseProfile';

export default function Home() {
  const [session, setSession] = useState(null);

  useEffect(() => {
    setSession(supabase.auth.session());

    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
  }, []);

  return <main>{!session ? <Login /> : <Profile session={session} />}</main>;
}
