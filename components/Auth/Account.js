import { useState, useEffect } from 'react';
import { supabase } from '../../pages/supabaseClient';
//import Avatar from './Avatar';

const Account = ({ session }) => {
    const [loading, setLoading] = useState(true);
    const [username, setUsername] = useState(null);
    const [website, setWebsite] = useState(null);
    const [avatar_url, setAvatarUrl] = useState(null);

    useEffect(() => {
        getProfile()
    }, [session]);

    const getProfile = async () => {
        try {
            setLoading(true);
            const user = supabase.auth.user();

            let { data, error, status } = await supabase
            .from('profiles')
            .select(`username, website, avatar_url`)
            .eq('id', user.id)
            .single()
            //setUserId(user.id)

            if (data) {
                setUsername(data.username);
                setWebsite(data.website);
                setAvatarUrl(data.avatar_url);
            }
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(false);
        }
    }

    const updateProfile = async (e) => {
        e.preventDefault();

        try {
            setLoading(true);
            const user = supabase.auth.user();
            const update = {
                id: user.id,
                username,
                website,
                avatar_url,
                updated_at: newDate()
            }

            let { error } = await supabase.from('profiles')
            .upsert(updates, { returning : 'minimal' })

            if (error) {
                throw error;
            }
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(false);
        }
    }
}