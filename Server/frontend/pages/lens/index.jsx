import Head from "next/head";
import Image from "next/image";
import styles from '../../styles/Home.module.css';
import { getFollowing, lensClient } from '../../constants/lensConstants';

let profileIdList = ['0x896c'];

export default function LensIndex() {
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
    };

    return (
        <div className={styles.container}>
            Hello!
        </div>
    )
}