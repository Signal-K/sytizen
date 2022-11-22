import React from "react";
import {
    ThirdwebNftMedia,
    useAddress,
    useContractRead,
    useMetadata,
    useTokenBalance,
    Web3Button,
} from "@thirdweb-dev/react";
import { SmartContract, Token } from "@thirdweb-dev/sdk";
import { ethers } from "ethers";
import styles from "../styles/Home.module.css";
import ApproxRewards from './ApproxRewards';

type Props = {
    miningContract: SmartContract<any>;
    tokenContract: Token;
};

export default function Rewards({ miningContract, tokenContract }: Props) {
    const address = useAddress();
    const { data: tokenMetadata } = useMetadata(tokenContract);
    const { data: currentBalance } = useTokenBalance(tokenContract, address);
    const { data: unclaimedAmount } = useContractRead(
        miningContract,
        "calculateRewards",
        [address]
    );
    const { mutate: claim } = useContractCall(miningContract, "claim");

    return (
        <div
            style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
        >
            <p>
                Your <b>Minerals</b>
            </p>

            {tokenMetadata && (
                <ThirdwebNftMedia
                // @ts-ignore
                    metadata={tokenMetadata}
                    height={"48"}
                />
            )}
            <p className={styles.noGapBottom}>
                Balance: <b>{currentBalance?.displayValue}</b>
            </p>
            <p>
                Unclaimed: {" "}
                <b>{unclaimedAmount && ethers.utils.formatUnits(unclaimedAmount)}</b>
            </p>
            <ApproxRewards miningContract={miningContract} />
            <Web3Button
                contractAddress={miningContract.getAddress()}
                action={() => claim([])}
            >
                Claim
            </Web3Button>
                
        </div>
    )
}