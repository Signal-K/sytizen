import { MediaRenderer } from '@thirdweb-dev/react';
import { useRouter } from 'next/router';
import React from 'react';
import FeedPost from '../../components/FeedPost';
import { useProfileQuery, usePublicationsQuery } from '../../graphql/generated';
import styles from '../../styles/Profile.module.css';

type Props = {}

export default function ProfilePage({}: Props) {
    const router = useRouter();
    const { id } = router.query;    
    const { isLoading: loadingProfile, data: profileData, error: profileError } = useProfileQuery({
        request: {
            handle: id,
        },
    }, {
        enabled: !!id,
    });

    const { isLoading: isLoadingPublications, data: publicationsData, error: publicationsError } = usePublicationsQuery({
        request: {
            profileId: profileData?.profile?.id
        },
    }, {
        enabled: !!profileData?.profile?.id,
    });

    if (publicationsError || profileError) {
        return <div>Couldn't find this profile</div>;
    }

    if (loadingProfile) {
        return <div>Loading profile...</div>
    }

    return (
        <div className={styles.profileContainer}>
            <div className={styles.profileContentContainer}>
                {/* @ts-ignore */}
                {profileData?.profile?.coverPicture?.original?.url && (
                        <MediaRenderer
                            // @ts-ignore
                            src={profileData?.profile?.coverPicture?.original?.url || ""}
                            alt={profileData.profile.name || profileData.profile.handle || ""}
                            className={styles.coverImageContainer}
                        />
                )}
                {/* @ts-ignore */}
                {profileData?.profile?.picture?.original?.url && (
                        <MediaRenderer
                            // @ts-ignore
                            src={profileData.profile.picture.original.url}
                            alt={profileData.profile.name || profileData.profile.handle || ""}
                            className={styles.profilePictureContainer}
                        />
                )}
                <h1 className={styles.profileName}>{profileData?.profile?.name || 'Unknown user'}</h1>
                <p className={styles.profileHandle}>{profileData?.profile?.handle}</p>
                <p className={styles.profileDescription}>{profileData?.profile?.bio}</p>
                <p className={styles.followerCount}>{profileData?.profile?.stats.totalFollowers} Followers</p>
            </div>
            <center><div className={styles.publicationsContainer}>
                {
                    publicationsData?.publications.items.map((publication) => (
                        <FeedPost publication={publication} key={publication.id} />
                    ))
                }
            </div></center>
    </div>
    )
}