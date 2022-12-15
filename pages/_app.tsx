import type { AppProps } from 'next/app';
import { ChainId, ThirdwebProvider } from '@thirdweb-dev/react';
import React from 'react';

const activeChainId = ChainId.Mumbai;
function MyApp({ Component, pageProps }: AppProps) {
    return (
        <ThirdwebProvider
            desiredChainId={activeChainId}
            authConfig={{
                domain: 'app.skinetics.tech',
                authUrl: '/api/auth',
                loginRedirect: '/',
            }}
        >
            <Component {...pageProps} />
        </ThirdwebProvider>
    );
}

export default MyApp;