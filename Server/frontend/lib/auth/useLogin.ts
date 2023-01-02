import { useMutation } from "@apollo/client";
import { useAddress, useSDK } from "@thirdweb-dev/react";
import { useAuthenticateMutation } from "../../graphql/generated";
import generateChallenge from "./generateChallenge";
import { setAccessToken } from "./helpers";

// Store access token inside local storage

export default function useLogin() {
    const address = useAddress(); // Ensure user has connected wallet
    const sdk = useSDK();
    const {
        mutateAsync: sendSignedMessage
    } = useAuthenticateMutation();

    async function login () {
        if (!address) {
            console.error('No address found. Please try connecting your wallet to continue signing into Lens');
            return null;
        }

        const { challenge } = await generateChallenge(address); // Generate challenge from the Lens API
        const signature = await sdk?.wallet.sign(challenge.text); // Sign the returned challenge with the user's wallet
        const { // Send the signed challenge to the Lens API
            authenticate
        } = await sendSignedMessage({
            request: {
                address,
                signature,
            },
        });

        const { accessToken, refreshToken} = authenticate;

        setAccessToken(accessToken, refreshToken);
    }

    // Receive an access token from Lens API
    return useMutation(login);
}