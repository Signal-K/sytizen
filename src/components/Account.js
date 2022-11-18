import { useState, useEffect } from "react"
import { supabase } from "../supabaseClient"
import Avatar from './Avatar';

// Styling imports =====>
import { Container } from "semantic-ui-react";

// API/data imports =====>
import { Planets } from "./api/Planets";
import { PlanetForm } from "./api/PlanetForm";

// Unity Views =====>
import { Unitydb } from "../controller/unity";

// Thirdweb && EVM components ======>
import { ConnectWallet, ThirdwebNftMedia, useContract, useNFTs, useOwnedNFTs, useAddress, Web3Button } from "@thirdweb-dev/react";

const Account = ( { session } ) => {
    // Authentication settings
    const [loading, setLoading] = useState(true)
    const [username, setUsername] = useState(null)
    const [website, setWebsite] = useState(null)
    const [avatar_url, setAvatarUrl] = useState(null)

    useEffect(() => {
        getProfile()
    }, [session]) // Update whenever session (from Supabase) changes


    // Planet/Other data states
    const [planetName, setPlanetName] = useState(null);
    const [planetId, setPlanetId] = useState(null);
    const [planetMoons, setPlanetMoons] = useState(0);
    const [planets, setPlanets] = useState([]);
    const [userId, setUserId] = useState(null);
    useEffect(() => {
        fetch('/planets').then(response => response.json().then(data => {
            setPlanets(data.planets);
        }));
    }, []); // Also pass in the authentication settings to Flask via POST

    /* Get planet information from Supabase
    const getPlanets = async () => {
        try {
            setLoading(true);
            let { data, error, status } = await supabase
            .from('planetsdemo') // From the planetsdemo table on Supabase
            .select(`planetid, name, moons`) // Select these values from the table
            .single()

            if (data) {
                setPlanetId(data.planetid);
                setPlanetName(data.name);
                setPlanetMoons(data.moons);
            }
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(false);
        }
    }*/

    // Get profile information from Supabase postgres
    const getProfile = async () => {
        try {
            setLoading(true)
            const user = supabase.auth.user()
            let { data, error, status } = await supabase
            .from('profiles')
            .select(`username, website, avatar_url`)
            .eq('id', user.id)
            .single()
            setUserId(user.id)

            if(data) {
                setUsername(data.username);
                setWebsite(data.website);
                setAvatarUrl(data.avatar_url);
            }
            console.log(user.id);
        } catch (error) {
            alert(error.message)
        }finally{
            setLoading(false)
        }
    }

    const updateProfile = async (e) => {
        e.preventDefault()

        try {
            setLoading(true)
            const user = supabase.auth.user();
            const updates = {
                id : user.id,
                username,
                website,
                avatar_url,
                updated_at: new Date()
            }

            let { error } = await supabase.from("profiles")
            .upsert(updates, { returning : 'minimal'})

            if(error){
                throw error;
            }
        } catch (error) {
            alert(error.message)
        } finally{
            setLoading(false)
        }
    }

    // Ethereum / Contract hooks ====>
    const { contract } = useContract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9"); // Add contract of collection as hook
    const address = useAddress(); // get the address of connected user
    const { data: nfts } = useOwnedNFTs(contract, address); // Array of nfts
  
    /* Game event hooks
    const { data: events } = useAllContractEvents(contract, {
      subscribe: true,
    });*/

    return (
        <div aria-live="polite" className='container mx-auto'>
      {loading ? (
        'Saving ...'
      ) : (
        <form onSubmit={updateProfile} className="form-widget">
            <Avatar
            url={avatar_url}
            size={150}
            onUpload={(url) => {
                setAvatarUrl(url)
                updateProfile({ username, website, avatar_url: url })
            }}
            />
          <div class="container mx-auto w-72 py-4">
                <input type="text" 
                name="text" 
                id="username"
                class="mt-1 px-3 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-md sm:text-sm focus:ring-1"
                placeholder="Your Name" 
                value={username || ''}
                onChange={(e) => setUsername(e.target.value)}
                />
          </div>
          <div class="container mx-auto w-72 py-4">
              <input type="text" 
              name="text" 
              class="mt-1 px-3 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-md sm:text-sm focus:ring-1" 
              placeholder="your@website.com"
              id="website"
              value={website || ''}
              onChange={(e) => setWebsite(e.target.value)}
              />
            </div>
          <div className='text-center'>
              <button class="w-44 h-11 rounded-full text-gray-50 bg-indigo-600 hover:bg-indigo-700" disabled={loading}>
                Update Profile
              </button>
          </div>
          <div className="text-center">
              <button type="button" className="button" onClick={() => supabase.auth.signOut()}>
                  Sign Out
              </button>
          </div>
        </form>
      )}
      <Container>
        <ConnectWallet />
        <hr />
        <Web3Button
            contractAddress={"0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9"}
            action={(contract) => contract.call("claim", address, 0, 1)} // Call claim function | 1 of token id 0
        >
            Claim a spaceship!
        </Web3Button>
        {nfts?.map((nft) => (<div>
            <ThirdwebNftMedia
                key={nft.metadata.id.toString()}
                metadata={nft.metadata}
            />
            <h2>{nft.metadata.name}</h2>
        </div>
        ))}

        <Planets planets={planets} />
        <PlanetForm />
        <p>The planet is {planetName} </p>
        <Unitydb />
      </Container>
    </div>
    )
}

export default Account;