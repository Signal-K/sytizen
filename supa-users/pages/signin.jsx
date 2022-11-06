import { MetaMaskConnector } from 'wagmi/connectors/metaMask';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useConnect, useAccount, useSignMessage, useDisconnect } from 'wagmi';
import axios from 'axios';

function SignIn() {
    const { connectAsync } = useConnect();
    const { disconnectAsync } = useDisconnect();
    const { isConnected } = useAccount();
    const { signMessageAsync } = useSignMessage();
    const { push } = useRouter();

    const handleAuth = async () => { // User attempts to authenticate themselves
        if (isConnected) { // Disconnect web3 provider if already active
            await disconnectAsync();
        }

        const { account, chain } = await connectAsync({ connector: new MetaMaskConnector() }); // Enable web3 provider for metamask
        const userData = { address: account, chain: chain.id, network: 'evm' };
        const { data } = await axios.post('/api/auth/request-message', userData, { // Make post request to 'request-message' endpoint
            headers: {
                'Content-Type': 'application/json',
            },
        })

        const message = data.message;
        const signature = await signMessageAsync({ message });

        console.log(userData);
        console.log(signature);

        // Redirect user after auth to /user
        const { url } = await signIn('credentials', { message, signature, redirect: false, callbackUrl: '/user' });
        push(url);
    };

    return (
        <div>
            <h3>Moralis Auth</h3>
            <button onClick={() => handleAuth()}>Authenticate via Metamask</button>
        </div>
    );
}

export default SignIn;