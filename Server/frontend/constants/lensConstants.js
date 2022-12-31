import { ApolloClient, InMemoryCache, gql } from "@apollo/client";

const API_URL = 'https://api.lens.dev';

export const lensClient = new ApolloClient({
    uri: API_URL,
    cache: new InMemoryCache(),
});

export const challenge = gql`
  query Challenge($address: EthereumAddress!) {
    challenge(request: { address: $address }) {
      text
    }
  }
`;

// Provide access & refresh token to determine Lens profile ID of the authenticated address
export const lensAuthenticate = gql`
  mutation Authenticate($address: EthereumAddress!, $signature: Signature!) {
    authenticate(request: { address: $address, signature: $signature }) {
      accessToken
      refreshToken
    }
  }
`;

export const getDefaultProfile = gql`
  query DefaultProfile($request: DefaultProfileRequest!) {
    defaultProfile(request: $request) {
        id
    }
  }
`;

export const getFollowing = gql`
  query Profile($request: FollowingRequest!) {
    following(request: $request) {
      items {
        profile {
          id
        }
      }
    }
  }
`;

// Query to show top profiles on the Protocol
export const exploreProfiles = gql`
  query ExploreProfiles {
    exploreProfiles(request: { sortCriteria: MOST_FOLLOWERS }) {
        items {
            id
            name
            bio
            handle
            picture {
                ... on MediaSet {
                    original {
                        url
                    }
                }
            }
            stats {
                totalFollowers
            }
        }
    }
  }
`;

export const getProfile = gql`
  query Profile($handle: Handle!) {
    id
    name
    bio
    picture {
        ...on MediaSet {
            original {
                url
            }
        }
    }
    handle
  }
`;

/* export const explore PublicationsVariables = {
    request: {
        sortCriteria: "LATEST",
        limit: 50,
    },
};

export const getExploredPublications = async function() {
    const exploredPublicationsResult = await apolloClient.query({
        query: explorePublications,
        variables: explorePublicationsVariables,
    });
    return exploredPublicationsResult;
};*/

export const getPublicationsQueryVariables = function (profileIds) {
    return {
        request: {
            limit: 5, // no more than 5 publications per request
            publicationTypes: "POST",
            metadata: {
                mainContentFocus: "ARTICLE",
            },
            profileIds: profileIds,
        },
    };
};

export const getPublications = gql`
  query Metadata($request: PublicationsQueryRequest!) {
    publications(request: $request) {
      items {
        ... on Post {
          id
          onChainContentURI
          profile {
            name
          }
          metadata {
            image
            name
          }
        }
      }
    }
  }
`;

export const getPublication = gql`
    query Metadata($request: PublicationQueryRequest!) {
        publication(request: $request) {
            ... on Post {
                metadata {
                    content
                    name
                    image
                }
                profile {
                    name
                }
            }
        }
    }
`;

export const getCreatePostQuery = function (profileId, contentUri) {
    console.log(profileId);
    console.log(contentUri);

    return gql`
        mutation CreatePostTypedData {
            createPostTypedData(
                request: {
                    profileId: "${profileId}"
                    contentURI: "${contentUri}"
                    collectModule: { freeCollectModule: { followerOnly: false } }
                    referenceModule: { followerOnlyReferenceModule: true }
                }
            ) {
                id
                expiresAt
                typedData {
                    types {
                        PostWithSig {
                            name
                            type
                        }
                    }
                    domain {
                        name
                        chainId
                        version
                        verifyingCOntract
                    }
                    value {
                        nonce
                        deadline
                        profileId
                        contentURI
                        collectModule
                        collectModuleInitData
                        referenceModule
                        referenceModuleInitData
                    }
                }
            }
        }
    `;
};

export const getListOfPublicationIds = async function (profileId) {
    const { data } = await lensClient.query({
        query: getPublications,
        variables: getPublicationsQueryVariables(profileId),
    });
    return data.publications.items.map((publication) => publication.id);
};

export const getPostResultById = async function (publicationId) {
    const postResult = await ApolloClient.query({
        query: getPublication,
        variables: {
            request: {
                publicationId: publicationId,
            },
        },
    });
    return postResult;
};

export const createContentMetadata = function (
    content,
    contentName,
    imageUri,
    imageType
) {
    return {
        version: "2.0.0",
        metadata_id: uuidv4(),
        description: "Created from LensBlog",
        content: content,
        name: contentName,
        mainContentFocus: "ARTICLE",
        attributes: [],
        locale: 'en-us',
        appId: 'lensBlog',
        image: imageUri,
        imageMimeType: imageType,
    };
};