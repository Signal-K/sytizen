// Styling imports
import '../styles/globals.css';

// Moralis + Supa | Moralis + Magic components
import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';
import { SessionProvider } from 'next-auth/react';

// Supabase + Magic components
import { useRouter } from 'next/router';
import { supabase } from './api/client';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { checkResultErrors } from 'ethers/lib/utils';

const { provider, webSocketProvider } = configureChains(defaultChains, [publicProvider()]);

const client = createClient({
  provider,
  webSocketProvider,
  autoConnect: true,
});

function MyApp({ Component, pageProps }) {
  const [authenticatedState, setAuthenticatedState] = useState('not-authenticated'); // auth state, retrieved from supa. defaults to not logged in
  const router = useRouter();

  useEffect(() => { // Set up supabase on/off auth state listener
    const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
      handleAuthChange(event, session);
      if (event === 'SIGNED_IN') { // This event only fires if the auth event occurs (e.g. being rerouted from the magic link that lands in their inbox)
        setAuthenticatedState('authenticated');
        router.push('/profile'); // Reroute user to profile if they're signed in
      }
      if (event === 'SIGNED_OUT') {
        setAuthenticatedState('not-authenticated');
      }
    })
    checkResultErrors();
    return () => {
      authListener.unsubscribe();
    }
  }, []);

  return (
    <WagmiConfig client={ client }>
      <SessionProvider session = {pageProps.session} refetchInterval={0}>
        <div>
          <nav></nav>
          <Component {...pageProps} />
        </div>
      </SessionProvider>
    </WagmiConfig>
  );
}

export default MyApp;