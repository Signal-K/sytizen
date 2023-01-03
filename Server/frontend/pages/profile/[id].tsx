import { useRouter } from 'next/router';
import React from 'react';
import { useProfileQuery, usePublicationsQuery } from '../../graphql/generated';
import styles from '../../styles/Profile.module.css';

type Props = {}

export default function ProfilePage({}: Props) {
    const router = useRouter();
    const { id } = router.query;    
    const { isLoading: loadingProfile, data: profileData } = useProfileQuery({
        request: {
            handle: id,
        },
    }, {
        enabled: !!id,
    });

    const { isLoading: isLoadingPublications, data: publicationsData } = usePublicationsQuery({
        request: {
            profileId: profileData?.profile?.id
        },
    }, {
        enabled: !!profileData?.profile?.id,
    });

    return (
        <div className={styles.profileContainer}>
            <div className={styles.profileContentContainer}>

            </div>
            <div className={styles.publicationsContainer}>

            </div>
    </div>
    )
}