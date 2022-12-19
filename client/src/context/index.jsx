import React, { useContext, createContext } from 'react';
import { useAddress, useContract, useMetamask, useContractWrite } from '@thirdweb-dev/react';
import { ethers } from 'ethers';

const StateContext = createContext();

export const StateContextProvider = ({ children }) => {
    const { contract } = useContract('0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004');
    const { mutateAsync: createProposal } = useContractWrite(contract, 'createProposal'); // Call function & create a proposal, passing in params from the form
    const address = useAddress();
    const connect = useMetamask();

    // Publish a proposal on-chain
    const publishProposal = async (form) => {
        try {
            const data = await createProposal([
                address, // Owner - creator of the campaign. useMetamask();
                form.title, // From CreateProposal.jsx
                form.description,
                form.target,
                new Date(form.deadline).getTime(),
                form.image,
            ]);

            console.log("Contract call success: ", data);
        } catch (error) {
            console.error('Contract call resulted in a failure, ', error)
        }
    }

    return(
        <StateContext.Provider
            value={{ address,
                contract,
                createProposal: publishProposal,
            }}
        >
            {children}
        </StateContext.Provider>
    )
}

// Hook to get the context returned to node frontend
export const useStateContext = () => useContext(StateContext);