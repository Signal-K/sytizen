import { useAddress, ConnectWallet, Web3Button, useContract, useNFTBalance } from '@thirdweb-dev/react';
import { useState, useEffect, useMemo } from 'react';
import styles from '../styles/Dao.module.css';

const Dao = () => {
    const address = useAddress();
    console.log("🤝 User address: ", address);

    if (!address) {
        return (
            <div className={styles.landing}>
                <h1>Welcome to Star Sailors DAO</h1>
                <div className={styles.btnhero}>
                    <ConnectWallet />
                </div>
            </div>
        );
    }

    const editionDropAddress = '0x93FC4ba29c41c059fB9f4727F3903df776771Af8';
    const { contract: editionDrop } = useContract(editionDropAddress, "edition-drop");
    const { data: nftBalance } = useNFTBalance(editionDrop, address, "0"); // Hook to check if authenticated user has membership nft
    const hasClaimedNFT = useMemo(() => {
        return nftBalance && nftBalance.gt(0);
    }, [nftBalance]);

    return (
        <div className={styles.landing}>
            <h1>👀 Mint your DAO membership</h1>
            <div className={styles.btnhero}>
                <Web3Button
                    contractAddress={editionDropAddress}
                    action={contract => {
                        contract.erc1155.claim(0, 1)
                    }}
                    onSuccess={() => {
                        console.log(`🌊 Successfully Minted! Check it out on OpenSea: https://testnets.opensea.io/assets/${editionDrop.getAddress()}/0`);
                    }}
                    onError={error => {
                        console.error("Failed to mint NFT, ", error);
                    }}
                >
                    Mint your membership NFT (FREE)
                </Web3Button>
            </div>
        </div>
    );
}

export default Dao;