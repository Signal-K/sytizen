import type { AppProps } from "next/app";
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MoralisProvider } from "react-moralis";
import Header from "../components/Header";

/*import Navbar from './lens/components/Navbar';
import { LensProvider } from '../context/lensContext';
import { ApolloProvider } from "@apollo/client";
import { lensClient } from './lens/constants/lensConstants';*/

function MyApp({ Component, pageProps }: AppProps) {
  const activeChainId = ChainId.Polygon; // Set to `.Mumbai` for testnet interaction
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
          <Header />
          <Component {...pageProps} />
        </MoralisProvider>
      </ThirdwebProvider>
    </QueryClientProvider>
  )
}

export default MyApp;