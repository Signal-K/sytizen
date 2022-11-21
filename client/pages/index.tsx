import type { NextPage } from "next";
import styles from '../styles/Home.module.css';
import { ConnectWallet, useAddress, useEditionDrop, useOwnedNFTs } from "@thirdweb-dev/react";
import { CHARACTERS_ADDRESS } from "../lib/contractAddresses";
import { useRouter } from "next/router";
import MintContainer from "../components/MintContainer";

const Home : NextPage = () => {
  const editionDrop = useEditionDrop(CHARACTERS_ADDRESS);
  const address = useAddress();
  const router = useRouter();

  const { // Get specific NFTs owned by the authenticated user based on the characters edition drop
    data: ownedNfts,
    isLoading,
    isError,
  } = useOwnedNFTs(editionDrop, address);

  if (!address) { // If user not connected, return the <ConnectWallet /> component
    return (
      <div className={styles.container}>
        <ConnectWallet />
      </div>
    )
  }

  if (isLoading) { // If we are retrieving the users' NFTs/eth state, display this
    return <div>Loading</div>;
  }
  if (!ownedNfts || isError) {
    return <div>Error</div>
  }

  if (ownedNfts.length === 0) { // If the user has no NFTs from the character collection
    return (
      <div className={styles.container}>
        <MintContainer />
      </div>
    )
  }

  return ( // If user already has an nft
    <div className={styles.container}>
      <button
        className={`${styles.mainButton} ${styles.spacerBottom}`}
        onClick={() => router.push(`/play`)}
      >
        Play game
      </button>
    </div>
  )
}

export default Home;