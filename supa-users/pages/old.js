// Component imports =====>
import Head from "next/head";
import Image from "next/image";
import { useEffect, useState } from "react";
import { supabase } from "../lib/initSupabase";
import Login from "../auth/Login";
import Profile from "../auth/Profile";

// Data imports ========>
import CountryList from '../components/countryList';

export default function Home() {
  const [session, setSession] = useState(null); // Authenticated sessions from Magic

  useEffect(() => {
    supabase.auth.onAuthStateChange((_event, session) => { // When auth status from supabase changes
      setSession(session); // set session to be auth session from sb
    }); // Connected to magic sdk
  }, []); // Runs only on mount

  return <main>{!session ? <Login /> : <Profile session={session} />}</main>;
}