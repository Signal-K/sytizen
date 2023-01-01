import Head from "next/head";
import Image from "next/image";
import styles from '../../styles/Home.module.css';
import { getFollowing, getPublications, getPublicationsQueryVariables, lensClient } from '../../constants/lensConstants';
import { useEffect, useState } from "react";
import { useMoralis } from "react-moralis";
import PostFeed from "../../components/PostFeed";

let profileIdList = ['0xa952'];

export default function LensIndex() {
    const [pubs, setPubs] = useState();
    const { account } = useMoralis();

    const getPublicationsList = async function () {
        let followings; // Who the user follows
        let followingsIds = []; // Array of profile IDs
        followings = await lensClient.query({
            query: getFollowing,
            variables: {
                request: { address: account }
            },
        });
        
        followingsIds = followings.data.following.items.map((f) => f.profile.id);

        profileIdList = profileIdList.concat(followingsIds);
        const publications = await lensClient.query({
            query: getPublications,
            variables: getPublicationsQueryVariables(profileIdList),
        });
        return publications;
    };

    useEffect(() => {
        if (account) {
            getPublicationsList().then((publications) => {
                console.log(publications);
                setPubs(publications);
            });
        }
    }, [account]);

    return (
        <div>
            <div className={styles.container}>Decentralised Proposals</div>
            {!pubs ? (
                <div>Loading...</div>
            ) : <div><PostFeed posts={pubs.data.publications.items} /> </div>}
        </div>
    )
}