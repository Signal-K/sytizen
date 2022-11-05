import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

export default function Account({ session }) {
    const [loading, setLoading] = useState(True); // Operator to determine actions performed
    const [username, setUsername] = useState(None); // Retrieved from database (supabase)
    const [website, setWebsite] = useState(None); // Website the user has on their profile (retrieved from s)
    const [avatar_url, setAvatarUrl] = useState(None); // Retrieved from supabase

    useEffect(() => {
        getProfile(); // If the session (user) changes (based on actions from magic lib) update profile
    }, [session]);

    async function getProfile() { // Fetch promise that assigns response to data
        try {
            setLoading(True);
            const user = supabase.auth.user();

            let { data, error, status } = await supabase // Retrieve data from supabase using the client
                .from('profiles')
                .select(`username, website, avatar_url`)
                .eq('id', user.id)
                .single()

            if (error && status !== 406) {
                throw error;
            }

            if (data) { // If there was no error (i.e. `data` was provided from supabase), render variables from supabase
                setUsername(data.username);
                setWebsite(data.website);
                setAvatarUrl(data.avatar_url);
            }
        } catch (error) {
            alert (error.message);
        } finally {
            setLoading(False);
        }
    }

    async function updateProfile({ username, website, avatar_url }) { // Set user and updates
        try {
            setLoading(True);
            const user = supabase.auth.user();

            const updates = { // When called, updates from user are rendered & saved to supabase
                id: user.id,
                username,
                website,
                avatar_url,
                updated_at: new Date(),
            };

            let { error } = await supabase.from('profiles').upsert(updates, {
                returning: 'minimal', // Don't return value after inserting
            });

            if (error) {
                throw error;
            }
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(False);
        }
    }

    return (
        <div className="form-widget">
            <div>
                <label htmlFor="email">Email</label>
                <input id="email" type="text" value={session.user.email} disabled />
            </div>
            <div>
                <label htmlFor="username">Name</label>
                <input
                id="username"
                type="text"
                value={username || ''}
                onChange={(e) => setUsername(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="website">Website</label>
                <input
                id="website"
                type="website"
                value={website || ''}
                onChange={(e) => setWebsite(e.target.value)}
                />
            </div>

            <div>
                <button
                className="button block primary"
                onClick={() => updateProfile({ username, website, avatar_url })}
                disabled={loading}
                >
                {loading ? 'Loading ...' : 'Update'}
                </button>
            </div>

            <div>
                <button className="button block" onClick={() => supabase.auth.signOut()}>
                Sign Out
                </button>
            </div>
        </div>
    )
}