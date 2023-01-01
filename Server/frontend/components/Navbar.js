import { ConnectButton } from "web3uikit";
import Link from "next/link";

export default function Navbar() {
    return (
        <ul>
            <Link href='/lens/'><li>Home</li></Link>
            <Link href='/lens/write-post'><li>Create Proposal</li></Link>
            <li>
                <div>
                    <ConnectButton moralisAuth={false} />
                </div>
            </li>
        </ul>
    )
};