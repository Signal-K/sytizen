import {
    ThirdwebNftMedia,
    useAddress,
    useOwnedNFTs,
    Web3Button,
} from "@thirdweb-dev/react";
import { EditionDrop, SmartContract } from "@thirdweb-dev/sdk";
import React from "react";
import LoadingSection from "./LoadingSection";
import styles from "../styles/Home.module.css";
import { BigNumber } from "ethers";
import { MINING_ADDRESS } from "../lib/contractAddresses";

type Props = {
    multitoolsContract: EditionDrop;
    miningContract: SmartContract<any>;
}

export default function OwnedGear({ multitoolsContract, miningContract }: Props) {
    const address = useAddress();
    const { data: ownedMultitools, isLoading } = useOwnedNFTs (
        multitoolsContract,
        address
    );

    if (isLoading) {
        return <LoadingSection />
    };

    async function equip(id: BigNumber) {
        if (!address) return;
        const hasApproval = await multitoolsContract.isApproved( // Is the contract approved by the account to be able to transfer the multitool?
            address,
            MINING_ADDRESS
        );

        if (!hasApproval) {
            await multitoolsContract.setApprovalForAll(MINING_ADDRESS, true);
        };

        await miningContract.call("stake", id);

        window.location.reload();
    }

    return (
        <>
            <div className={styles.nftBoxGrid}>
                {ownedMultitools?.map((p) => (
                    <div className={styles.nftBox} key={p.metadata.id.toString()}>
                        <ThirdwebNftMedia
                            metadata={p.metadata}
                            className={`${styles.nftMedia} ${styles.spacerTop}`}
                            height={"64"}
                        />
                        <h3>{p.metadata.name}</h3>

                        <Web3Button
                            contractAddress={MINING_ADDRESS}
                            action={() => equip(p.metadata.id)}
                        >
                            Equip
                        </Web3Button>
                    </div>
                ))}
            </div>
        </>
    );
}