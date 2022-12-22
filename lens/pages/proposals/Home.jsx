/*export { default as Home } from './Home';
export { default as Profile } from './Profile';
export { default as CreateProposal } from './CreateProposal';
export { default as ProposalDetails } from './ProposalDetails';*/

import React, { useState, useEffect } from "react";
import { useStateContext } from './context';
//import { DisplayProposals } from './components';

const Home = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [proposals, setProposals] = useState([]); // Empty array, retrieved from the state context from onchain

    const { address, contract, getProposals } = useStateContext(); /*
    const fetchProposals = async () => { // This is to allow us to call this g.request in the useEffect (as the request is async in /context)
        setIsLoading(true);
        const data = await getProposals();
        setProposals(data);
        setIsLoading(false);
    }

    useEffect(() => {
        if (contract) fetchProposals();
        console.log(proposals);
    }, [address, contract]); // Re-called when these change*/

    return (
        <div>Hello World</div>
    )
}

export default Home;