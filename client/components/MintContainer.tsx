import {
    useAddress,
    useClaimNFT,
    useEditionDrop,
    Web3Button,
} from "@thirdweb-dev/react";
import React from "react";
import { CHARACTERS_ADDRESS } from "../lib/contractAddresses";
import styles from "../styles/Home.module.css";
import rover from "../assets/rover.gif";

export default function MintContainer() {
    const editionDrop = useEditionDrop(CHARACTERS_ADDRESS);
    const { mutate: claim } = useClaimNFT(editionDrop); // Call the claim function when the user clicks on the button below
    const address = useAddress(); // mint the nft to this address/user

    return (
        <div className={styles.collectionContainer}>
            <h1>Claim NFT</h1>
            <p>Claim your Character NFT to start playing</p>
            <div className={`${styles.nftBox} ${styles.spacerBottom}`}>
                <img src="/rover.gif" style={{ height: 200 }} />
            </div>
            <Web3Button
                contractAddress={CHARACTERS_ADDRESS}
                action={() => {
                    claim ({
                        quantity: 1,
                        to: address!, // Currently connected wallet address
                        tokenId: 0,
                    });
                }}
                accentColor="#f5f"
                colorMode="dark"
            >
                Claim NFT
            </Web3Button>
        </div>
    )
}