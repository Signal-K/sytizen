import type { AppProps } from "next/app";
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import "../styles/globals.css";

const activeChainId = ChainId.Mumbai;

function MyApp({
  Component, pageProps
}: AppProps) {
  const AnyComponent = Component as any;
  
  return (
    <ThirdwebProvider desiredChainId={activeChainId}>
      <Component {...pageProps} />
    </ThirdwebProvider>
  )
}

export default MyApp;