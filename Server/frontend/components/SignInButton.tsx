import { useAddress, useNetworkMismatch, useNetwork, ConnectWallet, ChainId } from '@thirdweb-dev/react';
import React from 'react';
import useLensUser from '../lib/auth/useLensUser';
import useLogin from '../lib/auth/useLogin';

type Props = {};

export default function SignInButton({}: Props) {
    const address = useAddress(); // Detect connected wallet
    const isOnWrongNetwork = useNetworkMismatch(); // Is different to `activeChainId` in `_app.tsx`
    const [, switchNetwork] = useNetwork(); // Switch network to `activeChainId`
    const { isSignedInQuery, profileQuery } = useLensUser();
    const { mutate: requestLogin } = useLogin();
    
    // Connect wallet
    if (!address) {
        return (
            <ConnectWallet />
        );
    }

    // Switch network to polygon
    if (!isOnWrongNetwork) {
        return (
            <button
                onClick={() => switchNetwork?.(ChainId.Polygon)}
            >Switch Network</button>
        )
    }

    if (isSignedInQuery.isLoading) { // Loading signed in state
        return <div>Loading</div>
    }

    // Sign in with Lens
    if (!isSignedInQuery.data) { // Request a login to Lens
        return (
            <button
                onClick={() => requestLogin()}
            >Sign in with Lens</button>
        )
    };

    if (profileQuery.isLoading) { // Show user their Lens Profile
        return <div>Loading...</div>;
    };

    if (!profileQuery.data?.defaultProfile) { // If there's no Lens profile for the connected wallet
        return <div>No Lens Profile</div>;
    };

    if (profileQuery.data?.defaultProfile) { // If profile exists
        return <div>Hello {profileQuery.data?.defaultProfile?.handle} </div>
    };

    return (
        <div>Something went wrong</div>
    );
}