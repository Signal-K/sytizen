import { MagicAuthConnector } from "@everipedia/wagmi-magic-connector";
import { signIn } from "next-auth/react";
import { useAccount, useConnect, useSignMessage, useDisconnect } from "wagmi";
import { useRouter } from "next/router";
import axios from "axios";
//import '../../../src/assets/css/globals.css';
import { useState, useEffect } from 'react';
import { supabase } from '../api/auth/supabaseClient';
import Link from "next/link";

function SignIn() {
    // Moralis + Magic.link component
    const { connectAsync } = useConnect({
        connector: new MagicAuthConnector({
            options: {
                apiKey: 'pk_live_C337BC194C080B7D', // magic api key
            }
        })
    })
    const { disconnectAsync } = useDisconnect();
    const { isConnected } = useAccount();
    const { signMessageAsync } = useSignMessage();
    const { push } = useRouter();

    const handleAuth = async () => {
        if (isConnected) {
            await disconnectAsync();
        }

        const { account } = await connectAsync();
        const userData = { address: account, chain: '0x1', network: 'evm' }
        const { data } = await axios.post('/api/auth/request-message', userData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const message = data.message;
        const signature = await signMessageAsync({
            message
        });

        // Redirect user to '/dashboard' page after successful authentication/signin
        const { url } = await signIn('credentials', {
            message,
            signature,
            redirect: false,
            callbackUrl: '/dashboard',
        });
        push(url); // Get url from callback to prevent page refreshing
    }

    /* Supabase magic link
    const router = useRouter();
    const [authenticatedState, setAuthenticatedState] = useState('not-authenticated');
    useEffect(() => {
        const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
            handleAuthChange(event, session);
            if (event === 'SIGNED_IN') {
                setAuthenticatedState('authenticated');
                router.push('/dashboard')
            }
            if (event === 'SIGNED_OUT') {
                setAuthenticatedState('not-authenticated');
            }
        });
        checkUser();
        return () => {
            authListener.unsubscribe();
        }
    }, []);

    async function checkUser() {
        const user = await supabase.auth.user();
        if (user) {
            setAuthenticatedState('authenticated');
        }
    }

    async function handleAuthChange(event, session) {
        await fetch('/api/auth', {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/json' }),
            credentials: 'same-origin',
            body: JSON.stringify({ event, session }),
        });
    }*/

    return (
        <div>
            {/*<nav style={navStyle}>
                <Link href="/">
                    <a style={linkStyle}>Home</a>
                </Link>
                <Link href="/profile">
                    <a style={linkStyle}>Profile</a>
                </Link>
                {
                authenticatedState === 'not-authenticated' && (
                    <Link href="/sign-in">
                    <a style={linkStyle}>Sign In</a>
                    </Link>
                    )
                }
                <Link href="/protected">
                    <a style={linkStyle}>Protected</a>
                </Link>
            </nav>*/}
            <h3>Web3 authentication</h3>
            <button onClick={() => handleAuth()}>Authenticate via magic.link</button>
        </div>
    )
}

const navStyle = {
    margin: 20
}
  
const linkStyle = {
    marginRight: 10
}

export default SignIn;