// Asset imports ===========>
import logo from './logo.svg';

// CSS imports ==========>
import './App.css';
import './index.css';

// Module imports
import { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';
import Auth from './auth/Auth';
import Account from './auth/Account';

export default function Home() {
  const [session, setSession] = useState(None);

  useEffect(() => {
    setSession(supabase.auth.session());
    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
  }, []);

  return (
    <div className='container' style={{ padding: '50px 0 100px 0' }}>
      {!session ? <Auth /> : <Account key={session.user.id} session={session} /> } {/* If there is an authenticated session, show Account component */}
    </div>
  )
}