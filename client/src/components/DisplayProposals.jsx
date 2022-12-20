import React from 'react';
import { useNavigate } from 'react-router-dom';
import { loader } from '../assets';
import FundCard from './FundCard';

const DisplayProposals = ({ title, isLoading, proposals }) => {
    const navigate = useNavigate();

    const handleNavigate = (proposal) => {
        navigate(`/proposal-details/${proposal.title}`, { state: proposal })
    }

    return (
        <div>
            <h1 className='font-epilogue font-semibold text-[18px] text-white text-left'>{title}: ({proposals.length})</h1>
            <div className='flex flex-wrap mt-[20px] gap-[26px]'>
                {isLoading && (
                    <img src={loader} alt="loader" className='w-[100px] h-[100px] object-contain' />
                )}
                {!isLoading && proposals.length === 0 && ( // If there are no proposals matching the query
                    <p className='font-epilogue font-semibold text-[14px] leading-[39px] text-[#818183]'>
                        There are no proposals matching this query
                    </p>
                )}
                {!isLoading && proposals.length > 0 && proposals.map((proposal) => <FundCard
                    key={proposal.id}
                    {...proposal}
                    handleClick={() => handleNavigate(proposal)}
                />)}
            </div>
        </div>
    )
}

export default DisplayProposals;