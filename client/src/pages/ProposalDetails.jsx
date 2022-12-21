import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { ethers } from 'ethers';
import { useStateContext } from '../context';
import { CustomButton, CountBox } from '../components';
import { calculateBarPercentage, daysLeft } from '../utils';
import { thirdweb } from '../assets';

const ProposalDetails = () => {
  const { state } = useLocation();
  const { getVoters, contract, address } = useStateContext();
  console.log(state);

  const [isLoading, setIsLoading] = useState(false);
  const [amount, setAmount] = useState('');
  const [voters, setVoters] = useState([]); // Array of voters on a specific proposal
  const remainingDays = daysLeft(state.deadline);

  return (
    <div>
      {isLoading && 'Loading...'}
      <div className='w-full flex md:flex-row flex-col mt-10 gap-[30px]'>
        <div className='flex-1 flex-col'>
          <img src={state.image} alt='campaign' className='w-full h-[410px] object-cover rounded-xl' />
          <div className='relative w-full h-[5px] bg-[#3a3a43] mt-2'>
            <div className='absolute h-full bg-[#41cd8d]' style={{ width: `${calculateBarPercentage(state.target, state.amountCollected)}%`, maxWidth: '100%' }}>
            </div>
          </div>
        </div>
        <div className='flex md:w-[150px] w-full flex-wrap justify-between gap-[30px]'>
          <CountBox title='Days Left' value={remainingDays} />
          <CountBox title={`Raised of ${state.target}`} value={state.amountCollected} />
          <CountBox title='Voters' value={voters.length} />
        </div>
      </div>
      <div className='mt-[60px] flex lg:flex-row flex-col gap-5'>
        <div className='flex-[2] flex flex-col gap-[40px]'>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>CREATOR:</h4>
            <div className='mt-[20px] flex flex-row items-center flex-wrap gap-[14px]'>
              <div className='w-[52px] h-[52px] flex items-center justify-center rounded-full bg-[#2c2f32] cursor-pointer'>
                <img src={thirdweb} alt='user profilepic' className='w-[60%] h-[60%] object-contain' />
              </div>
              <div>
                <h4 className='font-epilogue font-semibold text-[14px] text-white break-all'>{state.owner}</h4>
                <p className='mt-[4px] font-epilogue font-normal text-[12px] text-[#808191]'>10 Proposals</p>
              </div>
            </div>
          </div>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>STORY:</h4>
            <div className='mt-[20px]'>
              <p className='font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify'>{state.description}</p>
            </div>
          </div>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>VOTERS:</h4>
            <div className='mt-[20px] flex flex-col gap-4'>
              {voters.length > 0 ? voters.map((item, index) => {
                <div>
                  VOTER
                </div>
              }) : (
                <p className='font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify'>Nobody has voted on this proposal yet</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProposalDetails;