import FeedPost from "../components/FeedPost";
import { PublicationMainFocus, PublicationSortCriteria, useExplorePublicationsQuery } from "../graphql/generated";
import styles from '../styles/Home.module.css';
import Sidebar from '../components/Sidebar';
import { useState, useEffect } from "react";

/* Proposals (Lens add-on) contract interaction
//import { useStateContext, /*getProposals*//* } from '../context/index';
//import { useContract, useContractRead } from "@thirdweb-dev/react";
//import allProposals from './api/proposals/fetchProposals';*/

export default function Home () {
  //console.log(allProposals);

  // Get publications from Lens
  const { isLoading, error, data } = useExplorePublicationsQuery({
    request: {
      sortCriteria: PublicationSortCriteria.Latest,
      metadata: {
        //mainContentFocus: PublicationSortCriteria.Latest,
      }
    },
  },
  {
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });

  // Get proposals from contract (which will later be attached to Lens as a custom module)
  

  if (isLoading) {
    return (<div className={styles.container}>Loading</div>)
  };

  if (error) {
    return (<div className={styles.container}>Error</div>)
  };

  return (
    <div>
      <div className='sm:flex hidden mr-10 relative'>
        <Sidebar />
      </div>
      <div className='flex-1 max-sm:w-full max-w:[1280px] mx-auto sm:pr-5'>
        <div className={styles.container}>
          <div className={styles.postsContainer}>
            {data?.explorePublications.items.map((publication) => (
              <FeedPost publication={publication} key={publication.id} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};