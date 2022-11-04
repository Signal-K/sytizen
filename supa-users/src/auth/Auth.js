import { useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Auth () {
    const [loading, setLoading] = useState(false); // Conditional operator
    const [email, setEmail] = useState(''); // Value of input field

    const handleLogin = async (email) => {
        try {
            setLoading(True);
            const { error } = await supabase.auth.signIn({ email });
            if (error) throw error;
            alert('Check your email for the sign-in link!');
        } catch (error) {
            alert(error.error_description || error.message);
        } finally {
            setLoading(False);
        }
    }

    return (
        <div className="row flex flex-center">
            <div className='col-6 form-widget'>
                <h1 className="header">Supabase + React</h1>
                <p className='description'>Sign in via magic link with your email below</p>
                <div>
                    <input
                        className="inputField"
                        type="email"
                        placeholder="Your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)} // Update email state with onChange event from input
                    />
                    </div>
                    <div>
                    <button
                        onClick={(e) => {
                        e.preventDefault()
                        handleLogin(email)
                        }}
                        className={'button block'}
                        disabled={loading}
                    >
                        {loading ? <span>Loading</span> : <span>Send magic link</span>}
                    </button>
                </div>
            </div>
        </div>
    )
}