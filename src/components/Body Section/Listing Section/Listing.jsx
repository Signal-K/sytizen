import React from 'react';
import './listing.css';

// Icon & Asset imports ===>
import { BsArrowRightShort } from 'react-icons/bs';
import { AiFillHeart } from 'react-icons/ai';
import tesspic from '../../../Assets/StatElements/TessStat.png';

const Listing = () => {
  return (
    <div className='listingSection'>
      <div className='heading flex'>
        <h1>My Listings</h1>
        <button className='btn flex'>
          See All <BsArrowRightShort className='icon' />
        </button>
      </div>
      <div className='secContainer flex'>
        <div className='singleItem'>
          <AiFillHeart className='icon' />
          <img src={tesspic} alt="Tess telescope" /> {/* Replace with pic of drone/rover/mineral */}
          <h3>Annual Spread</h3>
        </div>
      </div>
    </div>
  )
}

export default Listing;