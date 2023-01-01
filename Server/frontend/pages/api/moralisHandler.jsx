import '../styles/globals.css';
import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';

const { provider, webSocketProvider } = configureChains(defaultChains, [publicProvider()]);

const client = createClient({
  provider,
  webSocketProvider,
  autoConnect: true,
});

function MoralisHandle({ Component, pageProps }) {
  return
    <WagmiConfig client={client}>
      <Component {...pageProps} />
    </WagmiConfig>
}

export default MoralisHandle; /*
import '../styles/globals.css';
import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';

const { provider, webSocketProvider } = configureChains(defaultChains, [publicProvider()]);

const client = createClient({
  provider,
  webSocketProvider,
  autoConnect: true,
});

function MyApp({ Component, pageProps }) {
  return
    <WagmiConfig client={client}>
      <Component {...pageProps} />
    </WagmiConfig>
}

export default MyApp;*/