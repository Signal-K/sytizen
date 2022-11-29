import { useContract } from '@thirdweb-dev/react'

export default function InitProposals() {
    const { contract } = useContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", "vote")

    const proposals = contract.getAll();
    console.log(proposals);

    return(
        <div>
            Hello
        </div>
    )
}