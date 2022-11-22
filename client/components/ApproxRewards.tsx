import { useAddress } from "@thirdweb-dev/react";
import { SmartContract } from "@thirdweb-dev/sdk";
import { ethers } from "ethers";
import React, { useEffect, useState } from 'react';
import ContractMappingResponse from "../lib/ContractMappingResponse";

type Props = {
    miningContract: SmartContract<any>;
};

export default function ApproxRewards({ miningContract }: Props) {
    const address = useAddress();
    const everyMillisecondAmount = parseInt(
        (10_000_000_000_000 / 2.1).toFixed(0)
    );
    const [amount, setAmount] = useState<number>(0);
    const [multiplier, setMultiplier] = useState<number>(0); // for calculation of rewards, this matches the method from the contract

    useEffect(() => {
        (async () => {
            if (!address) return;
            const p = (await miningContract.call(
                "playerMultitool",
                address
            )) as ContractMappingResponse;

            if (p.isData) { // If the user does have an nft (multitool) staked
                setMultiplier(p.value.toNumber() + 1);
            } else {
                setMultiplier(0);
            }
        })();
    }, [address, miningContract]);

    useEffect(() => {
        const interval = setInterval(() => {
            setAmount(amount + everyMillisecondAmount); // Update amount of tokens earned
        }, 100);
        return () => clearInterval(interval);
    }, [amount, everyMillisecondAmount]);

    return (
        <p style={{ width: 370, overflow: "hidden" }}>
            Earned this session: {" "}
            <b>
                {ethers.utils.formatEther((amount * multiplier).toFixed(0)) || "Error..."}
            </b>
        </p>
    )
}