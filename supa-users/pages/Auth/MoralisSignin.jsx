import { useConnect } from 'wagmi';
import { InjectedConnector } from 'wagmi/connectors/injected';
import axios from 'axios';

function SignIn() {
    const { connectAsync } = useConnect();

    const handleAuth = async () => {
        const { account, chain } = await connectAsync({ connector: new InjectedConnector() });
        const userData = { address: account, chain: chain.id, network: 'evm' };
        console.log(userData);
    };

    return (
        <div>
            <h3>Moralis Auth</h3>
            <button
                onClick={() => handleAuth()}>Authenticate via Metamask
            </button>
        </div>
    );
}

export default SignIn;