import type { AppProps } from "next/app";
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import Navbar from './lens/components/Navbar';
import { MoralisProvider } from "react-moralis";
import { LensProvider } from '../context/lensContext';
import { ApolloProvider } from "@apollo/client";
import { lensClient } from './lens/constants/lensConstants';
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const activeChainId = ChainId.Mumbai;

function MyApp({ Component, pageProps }: AppProps) {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <ThirdwebProvider 
        desiredChainId={activeChainId}
        authConfig={{
          domain: "sailors.skinetics.tech",
          authUrl: "/api/auth",
          loginRedirect: "/"
        }}
      >
        <MoralisProvider initializeOnMount={false}>
              <Component {...pageProps} />
        </MoralisProvider>
      </ThirdwebProvider>
    </QueryClientProvider>
  )
}

export default MyApp;