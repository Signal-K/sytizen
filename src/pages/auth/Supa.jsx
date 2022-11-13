import { useState, useEffect } from "react";
import { supabase } from '../api/auth/supabaseClient';

export default function SupabaseLogin() {
    const [session, setSession] = useState(null);
  
    useEffect(() => {
        setSession(supabase.auth.session());

        supabase.auth.onAuthStateChange((_event, session) => {
        setSession(session);
        });
    }, []);

    return <main>{!session ? 'Show login' : 'show profile'}</main>;
}