// Styling imports
import '@shoelace-style/shoelace/dist/themes/light.css';
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path';

import { useEffect, useState } from 'react';
import './App.css';

// Auth component imports
import { supabase } from './supabaseClient'
import Auth from './components/Auth';
import Account from './components/Account';

// Thirdweb/EVM connector
import { ChainId, ThirdwebProvider } from '@thirdweb-dev/react';
const activeChainId = ChainId.Mumbai;

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.0.0-beta.83/dist/');

function App({ Component, pageProps }) {

  const [session, setSession] = useState(null)

  useEffect(() =>{
    setSession(supabase.auth.session())
    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })
  }, [])

  return (
    <ThirdwebProvider desiredChainId={activeChainId}>
      <div className="container mx-auto">
        {!session ? <Auth /> : <Account key={session.user.id} session={session} />}
      </div>
    </ThirdwebProvider>
  );
}

export default App;