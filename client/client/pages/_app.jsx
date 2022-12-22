import '../styles/globals.css';
import React from 'react';

// Imports for proposals/voting section
import { ProposalDetails, CreateProposal, Home, Profile } from './proposals/Home';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default MyApp;