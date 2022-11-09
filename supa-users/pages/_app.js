// Styling imports
import '../styles/globals.css';

// Moralis + Supa | Moralis + Magic components
import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';
import { SessionProvider } from 'next-auth/react';
import { useEffect, useState } from 'react';

const { provider, webSocketProvider } = configureChains(defaultChains, [publicProvider()]);

const client = createClient({
  provider,
  webSocketProvider,
  autoConnect: true,
});

function MyApp({ Component, pageProps }) {
  return (
    <WagmiConfig client={ client }>
      <SessionProvider session = {pageProps.session} refetchInterval={0}>
          <Component {...pageProps} /> {/* Save data from moralis id, then add to that their magic id */}
      </SessionProvider>
    </WagmiConfig>
  );
}

export default MyApp;