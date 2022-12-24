import '../styles/globals.css';
import React from 'react';
import Navbar from '../components/Navbar';
import { MoralisProvider } from 'react-moralis';

/* Imports for proposals/voting section
import { ProposalDetails, CreateProposal, Home, Profile } from './proposals/Home';*/

function MyApp({ Component, pageProps }) {
  return (
    <MoralisProvider initializeOnMount={false}>
      <Navbar />
      <Component {...pageProps} />
    </MoralisProvider>
  );
}

export default MyApp;