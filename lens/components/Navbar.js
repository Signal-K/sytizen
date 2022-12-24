import { ConnectButton } from '@web3uikit/web3';

export default function Navbar() {
    return (
        <div>
            <ConnectButton moralisAuth={false} /> {/* Not currently using Moralis servers for authentication (see `../server`) */}
            Hello World
        </div>
    )
}