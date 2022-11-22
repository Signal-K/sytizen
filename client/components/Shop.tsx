import { ThirdwebNftMedia, useNFTs } from "@thirdweb-dev/react";
import { EditionDrop } from "@thirdweb-dev/sdk";
import React, { useEffect } from "react";
import styles from "../styles/Home.module.css";
import ShopItem from './ShopItem';

type Props = {
    multitoolsContract: EditionDrop;
};

export default function Shop({ multitoolsContract }: Props) {
    const { data: availableMultitools } = useNFTs(multitoolsContract);

    return (
        <>
            <div className={styles.nftBoxGrid}>
                {availableMultitools?.map((p) => (
                    <ShopItem
                        multitoolsContract={multitoolsContract}
                        item={p}
                        key={p.metadata.id.toString()}
                    />
                ))}
            </div>
        </>
    );
}