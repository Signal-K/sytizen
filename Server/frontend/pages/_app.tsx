import type { AppProps } from "next/app";
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import Navbar from '../components/Navbar';
import { MoralisProvider } from "react-moralis";
import { LensProvider } from '../context/lensContext';
import { ApolloProvider } from "@apollo/client";
import { lensClient } from "../constants/lensConstants";

const activeChainId = ChainId.Mumbai;

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThirdwebProvider 
      desiredChainId={activeChainId}
      authConfig={{
        domain: "sailors.skinetics.tech",
        authUrl: "/api/auth",
        loginRedirect: "/"
      }}
    >
      <MoralisProvider initializeOnMount={false}>
        <ApolloProvider client={lensClient}>
          <LensProvider>
            <Navbar />
            <Component {...pageProps} />
          </LensProvider>
        </ApolloProvider>
      </MoralisProvider>
    </ThirdwebProvider>
  )
}

export default MyApp;