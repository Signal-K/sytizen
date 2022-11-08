import { getSession, signOut } from 'next-auth/react';

function User({ user }) { // Get this prop from getServerSideProps
    return (
        <div>
            <h4>User session:</h4>
            <pre>{JSON.stringify(user, null, 2)}</pre>
            <button onClick={() => signOut({ redirect: '/signin' })}>Sign out</button>
        </div>
    );
}

export async function getServerSideProps(context) {
    const session = await getSession(context);

    if (!session) { // Redirect if not authenticated
        return {
            redirect: {
                destination: '/signin',
                permanent: false,
            },
        };
    }

    return {
        props: { user: session.user }, // Get the user's connected wallets and pass them into Flask
    };
}

export default User;
