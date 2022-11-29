import { useNFTs } from "@thirdweb-dev/react";
import { EditionDrop } from "@thirdweb-dev/sdk";
import React from "react";
import styles from "../../styles/Home.module.css";
import ShopItem from "./ShopItem";

type Props = {
  multitoolContract: EditionDrop;
};

/**
 * This component shows the:
 * - All of the available multitools from the edition drop and their price.
 */
export default function Shop({ multitoolContract }: Props) {
  const { data: availablemultitools } = useNFTs(multitoolContract);

  return (
    <>
      <div className={styles.nftBoxGrid}>
        {availablemultitools?.map((p) => (
          <ShopItem
            multitoolContract={multitoolContract}
            item={p}
            key={p.metadata.id.toString()}
          />
        ))}
      </div>
    </>
  );
}
