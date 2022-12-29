import { ConnectButton } from "web3uikit";


export default function Navbar() {
    return (
        <ul>
            <li>Home</li>
            <li>Create Proposal</li>
            <li>
                <div>
                    <ConnectButton moralisAuth={false} />
                </div>
            </li>
        </ul>
    )
};