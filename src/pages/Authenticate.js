import { useState } from "react";
import { supabase } from "../lib/supabaseClient";

export default function SupabaseAuth() {
    const [email, setEmail] = useState('');
    const [submitted, setSubmitted] = useState(false);

    async function signIn() {
        const { error, data } = await supabase.auth.signIn({
            email
        });
        if (error) {
            console.log({ error });
        } else {
            setSubmitted(true);
        }
    }
    if (submitted) {
        return (
            <div>
                <h1>Please check your email to sign in</h1>
            </div>
        )
    };

    return (
        <div>
            <main>
                <h1>
                    Sign in
                </h1>
                <input
                    onChange={e => setEmail(e.target.value)}
                    style={{ margin: 10 }}
                />
                <button onClick={() => signIn()}>Sign In</button>
            </main>
        </div>
    )
}