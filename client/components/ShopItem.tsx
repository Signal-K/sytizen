import {
    NFT,
    ThirdwebNftMedia,
    useActiveClaimCondition,
    useAddress,
    useClaimNFT,
    Web3Button,
} from "@thirdweb-dev/react";
import { EditionDrop } from "@thirdweb-dev/sdk";
import { BigNumber, ethers } from "ethers";
import React from "react";
import styles from '../styles/Home.module.css';

type Props = {
    multitoolsContract: EditionDrop;
    item: NFT;
};

export default function ShopItem({ item, multitoolsContract }: Props) {
    const address = useAddress();
    const { data: claimCondition } = useActiveClaimCondition(
        multitoolsContract,
        item.metadata.id
    );
    const { mutate: claimNft } = useClaimNFT(multitoolsContract);

    async function buy(id: BigNumber) {
        if (!address) return;

        try {
            claimNft({
                to: address,
                tokenId: id,
                quantity: 1,
            });
        } catch (e) {
            console.error(e);
            alert("Something went wrong. You may not have enough minerals to craft this multitool")
        };
    }

    return (
        <div className={styles.nftBox} key={item.metadata.id.toString()}>
            <ThirdwebNftMedia
                metadata={item.metadata}
                className={`${styles.nftMedia} ${styles.spacerTop}`}
                height={"64"}
            />
            <h3>{item.metadata.name}</h3>
            <p>
                Price: {" "}
                <b>
                    {claimCondition && ethers.utils.formatUnits(claimCondition?.price)}{" "}
                    $MINERAL
                </b>
            </p>
            <Web3Button
                contractAddress={multitoolsContract.getAddress()}
                action={() => buy(item.metadata.id)}
            >
                Buy
            </Web3Button>
        </div>
    )
}