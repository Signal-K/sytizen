import {
  ConnectWallet,
  useAddress,
  useContract,
  useMetamask,
} from "@thirdweb-dev/react";
import React, { useEffect, useState } from "react";
import CurrentGear from "../components/Ansible/CurrentGear";
import LoadingSection from "../components/Ansible/LoadingSection";
import OwnedGear from "../components/Ansible/OwnedGear";
import Rewards from "../components/Ansible/Rewards";
import Shop from "../components/Ansible/Shop";
import {
  CHARACTER_EDITION_ADDRESS,
  GOLD_GEMS_ADDRESS,
  MINING_CONTRACT_ADDRESS,
  multitool_EDITION_ADDRESS,
} from "../lib/contractAddresses";
import styles from "../styles/Home.module.css";

import Dao from "../components/dao";
import Auth from "../components/Auth/Auth";
import { supabase } from "./supabaseClient";
import PlanetBreadboard from '../components/Controller/Planet';

// Communicate with the DAO
//import InitProposals from '../lib/Proposals/init';

export default function Play() {
  const address = useAddress();

  const { contract: miningContract } = useContract(MINING_CONTRACT_ADDRESS);
  const { contract: characterContract } = useContract(
    CHARACTER_EDITION_ADDRESS,
    "edition-drop"
  );
  const { contract: multitoolContract } = useContract(
    multitool_EDITION_ADDRESS,
    "edition-drop"
  );
  const { contract: tokenContract } = useContract(GOLD_GEMS_ADDRESS, "token");

  if (!address) {
    return (
      <div className={styles.container}>
        <ConnectWallet colorMode="dark" />
      </div>
    );
  }
  

  /* Supabase authentication components
  const [session, setSession] = useState(null);
  useEffect(() => {
    setSession(supabase.auth.session())
    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })
  }, [])*/

  return (
    <div className={styles.container}>
        {/*<Auth /> */}
        <ConnectWallet />
        <Dao />
        <PlanetBreadboard />
        {miningContract &&
        characterContract &&
        tokenContract &&
        multitoolContract ? (
          <div className={styles.mainSection}>
            <CurrentGear
              miningContract={miningContract}
              characterContract={characterContract}
              multitoolContract={multitoolContract}
            />
            <Rewards
              miningContract={miningContract}
              tokenContract={tokenContract}
            />
          </div>
        ) : (
          <LoadingSection />
        )}

        <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />

        {multitoolContract && miningContract ? (
          <>
            <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>
              Your Owned multitools
            </h2>
            <div
              style={{
                width: "100%",
                minHeight: "10rem",
                display: "flex",
                flexDirection: "row",
                justifyContent: "center",
                alignItems: "center",
                marginTop: 8,
              }}
            >
              <OwnedGear
                multitoolContract={multitoolContract}
                miningContract={miningContract}
              />
            </div>
          </>
        ) : (
          <LoadingSection />
        )}

        <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />

        {multitoolContract && tokenContract ? (
          <>
            <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>Shop</h2>
            <div
              style={{
                width: "100%",
                minHeight: "10rem",
                display: "flex",
                flexDirection: "row",
                justifyContent: "center",
                alignItems: "center",
                marginTop: 8,
              }}
            >
              <Shop multitoolContract={multitoolContract} />
            </div>
            
          </>
        ) : (
          <LoadingSection />
        )}
      </div>
    /*<div className="container mx-auto">
       {!session ? <Auth /> : <Account key={session.user.id} session={session} />} 
      Maybe move everything below into a new component, and then set that component in the place of <Account key.... />
      */
  );
}
