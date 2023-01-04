import FeedPost from "../components/FeedPost";
import { PublicationMainFocus, PublicationSortCriteria, useExplorePublicationsQuery } from "../graphql/generated";
import styles from '../styles/Home.module.css';
import { useState, useEffect } from "react";
import Sidebar from '../components/Navigation/Sidebar';
import { Flex, Text, IconButton } from '@chakra-ui/react';

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
    <Flex w='100%'>
      <Sidebar />
      <Flex
        pos="absolute"
        top="50%"
        left="50%"
        transform="translate(-50%, -50%)"
      >
        <div className={styles.container}>
          <div className={styles.postsContainer}>
            {data?.explorePublications.items.map((publication) => (
              <FeedPost publication={publication} key={publication.id} />
            ))}
          </div>
        </div>
      </Flex>
    </Flex>
  );
};