import { fetcher } from "../../graphql/auth-fetcher";
import { RefreshMutation, RefreshMutationVariables, RefreshDocument } from "../../graphql/generated";
import { readAccessToken, setAccessToken } from "./helpers";

export default async function refreshAccessToken () { // Take current refresh, access token to Lens to generate a new Access token
    // Read refresh token from local storage
    const currentRefreshToken = readAccessToken()?.refreshToken;
    if (!currentRefreshToken) return null;

    // Send refresh token to Lens
    const result = await fetcher<RefreshMutation, RefreshMutationVariables>(RefreshDocument, {
            request: {
                refreshToken: currentRefreshToken
            },
        })();

    // Set new refresh token
    const { 
        accessToken, refreshToken: newRefreshToken
    } = result.refresh;
    setAccessToken(accessToken, newRefreshToken);

    return accessToken as string;
}