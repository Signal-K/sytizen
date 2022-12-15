import { useAddress, useDisconnect, useUser, useLogin, useLogout, useMetamask } from "@thirdweb-dev/react";
import type { NextPage } from "next";
import React from "react";

const Home: NextPage = () => {
    const address = useAddress();
    const connect = useMetamask();
    const disconnect = useDisconnect();
    const login = useLogin();
    const logout = useLogout();
    const { user } = useUser();

    return (
        <div>
            {address ? ( // If page is loaded with an address connected
                <>
                    <button onClick={disconnect}>Disconnect Wallet</button>
                    <button onClick={() => login()}>Login with Wallet</button>
                    <button onClick={logout}>Logout</button>
                    <p>Your address: {address}</p>
                    <pre>User: {JSON.stringify(user || null, undefined, 2)}</pre>
                </>
            ) : (
                <button onClick={connect}>Connect Wallet</button>
            )}
        </div>
    );
};

export default Home;