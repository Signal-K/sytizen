import { useState, useEffect, createContext, useContext } from "react";
import { challenge, lensClient, lensAuthenticate, getDefaultProfile } from '../constants/lensConstants';
import { useMoralis } from "react-moralis";
import { ethers } from "ethers";

export const lensContext = createContext();
export const useLensContext = () => {
    return useContext(lensContext);
}

export function LensProvider({ children }) {
    const [profileId, setProfileId] = useState();
    const [token, setToken] = useState();
    const { account } = useMoralis();

    const signIn = async function () {
        try {
            const challengeInfo = await lensClient.query({
                query: challenge,
                variables: { address: account },
            });

            const provider = new ethers.providers.Web3Provider(window.ethereum);
            const signer = provider.getSigner();
            const signature = await signer.signMessage(challengeInfo.data.challenge.text);

            const authData = await lensClient.mutate({
                mutation: lensAuthenticate,
                variables: {
                    address: account,
                    signature,
                },
            });

            const {
                data: {
                    authenticate: { accessToken },
                },
            } = authData;
            setToken(accessToken);
            console.log(accessToken);
        } catch (error) {
            console.error("Error signing in, ", error);
        }
    };

    const getProfileId = async function () {
        const defaultProfile = await lensClient.query({
            query: getDefaultProfile,
            variables: {
                request: {
                    ethereumAddress: account,
                },
            },
        });

        if (defaultProfile.data.defaultProfile) {// Check to see if the connected wallet has a lens acct
            console.log(defaultProfile.data.defaultProfile.id)
            return defaultProfile.data.defaultProfile.id;
        }
        return null;
    }

    useEffect(() => {
        const readToken = window.localStorage.getItem("lensToken");
        if (readToken) {
            setToken(readToken);
        }

        if (account && !token && !readToken) {
            signIn();
        }

        if (!account) {
            window.localStorage.removeItem("lensToken");
        }

        if (account) {
            getProfileId().then((id) => setProfileId(id));
        }
    }, [account]);

    useEffect(() => {
        if (token) {
            window.localStorage.setItem("lensToken", token);
        }
    }, [token]); // Whenever the token changes

    return (
        <lensContext.Provider value={{ profileId, token }}>
          {children}
        </lensContext.Provider>
    );
}