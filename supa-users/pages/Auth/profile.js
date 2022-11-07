import { useState, useEffect } from "react";
import { supabase } from "../api/client";
import { useRouter } from "next/router";

export default function Profile() {
    const [profile, setProfile] = useState(null);
    const router = useRouter();

    useEffect(() => {
        fetchProfile();
    }, []);

    async function fetchProfile() {
        const profileData = await supabase.auth.user(); // Returns null if user isn't signed in
        if (!profileData) {
            router.push('/auth/signin');
        } else { // If there is a profile (user signed in)
            setProfile(profileData);
        }
    }

    async function signOut() {
        await supabase.auth.signOut();
        router.push('/auth/signin');
    }

    if (!profile) return null;
    
    return ( // if (profile)
        <div style={{ maxWidth: '420px', margin: '96px auto' }}>
            <h2>Hello, {profile.email}</h2>
            <p>User ID: {profile.id}</p>
            <button onClick={signOut}>Sign Out</button>
        </div>
    )
}