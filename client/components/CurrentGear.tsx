import { ThirdwebNftMedia, useAddress, useNFT } from "@thirdweb-dev/react";
import { EditionDrop, SmartContract } from "@thirdweb-dev/sdk";
import React, { useEffect, useState } from "react";
import ContractMappingResponse from "../lib/ContractMappingResponse";
import EditionDropMetadata from "../lib/EditionDropMetadata";
import GameplayAnimation from './GameplayAnimation';
import styles from '../styles/Home.module.css';

type Props = {
    miningContract: SmartContract<any>;
    characterContract: EditionDrop;
    multitoolsContract: EditionDrop;
};

export default function CurrentGear({ // Shows the currently equipped character and multitool
    miningContract, characterContract, multitoolsContract,
}: Props) {
    const address = useAddress(); // Load currently connected wallet
    const { data: playerNft } = useNFT(characterContract, 0); // Load the nft in the player's wallet with token id 0 from the collection
    const [multitool, setMultitool] = useState<EditionDropMetadata>(); // Store the multitool that the user currently is staking (if they're staking one)

    useEffect(() => {
        (async () => {
            if (!address) return; // If no address, can't load anything, so return null

            const p = (await miningContract.call( // Return token id in the user's wallet 
                "playerMultitool",
                address
            )) as ContractMappingResponse; // Return statement determining if user is staking multitool

            if (p.isData) { // Fetch & load metadata from staked contract (if it is being staked, as isData will otherwise be null)
                const multitoolMetada = await multitoolsContract.get(p.value);
                setMultitool(multitoolMetada);
            }
        })();
    }, [address, miningContract, multitoolsContract]); // Whenever any variable here changes, refresh/load the page

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <h2 className={`{styles.noGapTop}`}>Equipped Items</h2>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    flexDirection: "row",
                    justifyContent: "center",
                }}
            >
                <div style={{ outline: "1px solid grey", borderRadius: 16 }}> {/* Currently equipped items */}
                    {playerNft && (
                        <ThirdwebNftMedia metadata={playerNft?.metadata} height={"64"} /> // Render metadata of currently equipped nft 
                    )}
                </div>
                <div // Currently equipped multitool
                    style={{ outline: "1px solid grey", borderRadius: 16, marginLeft: 8 }}
                >
                    {multitool && (
                        // @ts-ignore
                        <ThirdwebNftMedia metadata={multitool.metadata} height={"64"} />
                    )}
                </div>
            </div>
            <div // Gameplay animation -> work in W,A,S,D somehow later
                style={{
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center",
                    justifyContent: "center",
                    marginTop: 24,
                }}
            >
                <img src="./rover.gif" height={64} width={64} alt="character-mining" />
                <GameplayAnimation multitool={multitool} />
            </div>
        </div>
    )
}