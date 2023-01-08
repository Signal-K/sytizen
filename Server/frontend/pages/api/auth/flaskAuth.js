import type { NextPage } from "next";
import useAuthenticate from '../../../hooks/useAuthenticate';
import { useAddress, useDisconnect, useUser, useLogin, useLogout, useMetamask } from "@thirdweb-dev/react";
import { useState } from "react";

// Lens Client
import { MoralisProvider } from "react-moralis";
import { LensProvider } from '../../lens/context/lensContext';
import { ApolloProvider } from "@apollo/client";
import { lensClient } from '../../lens/constants/lensConstants';
import { ChainId, ThirdwebProvider } from "@thirdweb-dev/react";
import Navbar from "../../lens/components/Navbar";

// FlaskAuth functional component should be moved to `pages/index.tsx` to see Flask auth in action

const activeChainId = ChainId.Mumbai;

const FlaskAuth: NextPage = () => {
  const address = useAddress();
  const disconnect = useDisconnect();
  const connectWithMetamask = useMetamask();
  const { login, authenticate, logout } = useAuthenticate();
  const loginSupa = useLogin();
  const logoutSupa = useLogout();
  const { user } = useUser();

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authMessage, setAuthMessage] = useState("N/A");

  const signInWithEthereum = async () => {
    setAuthMessage("N/A");
    await connectWithMetamask();
    await login();
    setIsLoggedIn(true);
  }

  const authenticatedRequest = async () => {
    const res = await authenticate();
    
    if (res.ok) {
      const address = await res.json();
      setAuthMessage(`Succesfully authenticated to backend with address ${address}`);
    } else {
      setAuthMessage(`Failed to authenticate, backend responded with ${res.status} (${res.statusText})`);
    }
  }

  const logoutWallet = async () => {
    await logout();
    setIsLoggedIn(false);
    setAuthMessage("N/A");
  }

  return (
    <ApolloProvider client={lensClient}>
        <LensProvider>
            <div>
                <Navbar />
            <h2>Wallet connection with Flask (frontend)</h2>
            {address ? (
                <button onClick={disconnect}>Disconnect Wallet</button>
            ) : (
                <button onClick={connectWithMetamask}>Connect Wallet</button>
            )}
            <p>Connected Address: {address || "N/A"}</p>

            <h2>Authentication - backend</h2> {/* Send this info to Supabase via Python */}
            
            {address ? (
                <>
                {isLoggedIn ? (
                    
                    <div>
                    <button onClick={logoutWallet}>Logout</button>
                    
                    {/* Supabase auth handler */}
                    <br />
                    <button onClick={() => loginSupa()}>Login with Supabase</button>
                    <button onClick={logoutSupa}>Logout Supabase</button>
                    <pre>User: {JSON.stringify(user || null, undefined, 2)}</pre>
                    </div>
                    ) : (
                    <button onClick={signInWithEthereum}>Login with wallet</button>
                )}

                <button onClick={authenticatedRequest}>Authenticate</button>

                <p>Logged in Address: { isLoggedIn ? address : "N/A" }</p>
                <p>Authentication: { authMessage }</p>
                </>
            ) : (
                <>Connect your wallet to access authentication</>
            )}
            </div>
        </LensProvider>
    </ApolloProvider>
  );
};

export default FlaskAuth;