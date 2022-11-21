import {
    ConnectWallet,
    useAddress,
    useContract,
    useEditionDrop,
    useToken,
} from "@thirdweb-dev/react";
import React from "react";
import CurrentGear from '../components/CurrentGear';
import LoadingSection from "../components/LoadingSection";
import OwnedGear from "../components/OwnedGear";
import Rewards from "../components/Rewards";
import Shop from "../components/Shop";
import {
    CHARACTERS_ADDRESS,
    MINERALS_ADDRESS,
    MINING_ADDRESS,
    MULTITOOLS_ADDRESS
} from "../lib/contractAddresses";
import styles from "../styles/Home.module.css";

export default function Play() {
    const address = useAddress();
    const { contract: miningContract } = useContract(MINING_ADDRESS);
    const characterContract = useEditionDrop(CHARACTERS_ADDRESS);
    const multitoolsContract = useEditionDrop(MULTITOOLS_ADDRESS);
    const tokenContract = useToken(MINERALS_ADDRESS);

    if (!address) { // If user isn't connected, display the "connect wallet" button component
        return (
            <div className={styles.container}>
                <ConnectWallet />
            </div>
        )
    }

    // Main gameplay screen/component
    return (
        <div className={styles.container}>
            {miningContract &&
            characterContract &&
            tokenContract &&
            multitoolsContract ? (
                <div className={styles.mainSection}>
                    <CurrentGear
                        miningContract={miningContract}
                        characterContract={characterContract}
                        multitoolsContract={multitoolsContract}
                    />
                    <Rewards
                        miningContract={miningContract}
                        tokenContract={tokenContract}
                    />
                </div>
            ) : ( // Display loading section if the contracts aren't loaded in/connected to yet
                <LoadingSection />
            )}

            <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />
            {multitoolsContract && miningContract ? (
                <>
                    <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>
                        Your owned multitools
                    </h2>
                    <div className={styles.shop}>
                        <OwnedGear
                            multitoolsContract={multitoolsContract}
                            miningContract={miningContract}
                        />
                    </div>
                </>
            ) : (
                <LoadingSection />
            )}

            <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />

            {multitoolsContract && tokenContract ? ( // Show shop here
                <>
                    <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>Shop</h2>
                    <div className={styles.shop}>
                        <Shop multitoolsContract={multitoolsContract} />
                    </div>
                </>
            ) : (
                <LoadingSection />
            )}
        </div>
    );
}