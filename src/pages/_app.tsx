import type { AppProps } from 'next/app';
import type { NextPageWithLayout } from '@/types';
import { useEffect, useState } from 'react';
import Head from 'next/head';
import { Hydrate, QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { ThemeProvider } from 'next-themes';
import ModalsContainer from '@/components/modal-views/container';
import DrawersContainer from '@/components/drawer-views/container';
import SettingsButton from '@/components/settings/settings-button';
import SettingsDrawer from '@/components/settings/settings-drawer';
import { WalletProvider } from '@/lib/hooks/use-connect';
import 'overlayscrollbars/css/OverlayScrollbars.css';
// base css file
import 'swiper/css';
import '@/assets/css/scrollbar.css';
import '@/assets/css/globals.css';
import '@/assets/css/range-slider.css';

import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';
import { SessionProvider } from 'next-auth/react';

// Supabase imports
import { createBrowserSupabaseClient } from '@supabase/auth-helpers-nextjs';
import { SessionContextProvider, Session } from '@supabase/auth-helpers-react';

const { provider, webSocketProvider } = configureChains(defaultChains, [publicProvider()]);
const client = createClient({
  provider,
  webSocketProvider,
  autoConnect: true,
})

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
};

function CustomApp({ Component, pageProps }: AppPropsWithLayout) {
  const [queryClient] = useState(() => new QueryClient());
  const getLayout = Component.getLayout ?? ((page) => page);

  //could remove this if you don't need to page level layout
  return (
    <WagmiConfig client = { client }>
      <SessionProvider session = {pageProps.session} refetchInterval={0}>
        <>
          <Head>
            {/* maximum-scale 1 meta tag need to prevent ios input focus auto zooming */}
            <meta
              name="viewport"
              content="width=device-width, initial-scale=1 maximum-scale=1"
            />
          </Head>
          <QueryClientProvider client={queryClient}>
            <Hydrate state={pageProps.dehydratedState}>
              <ThemeProvider
                attribute="class"
                enableSystem={false}
                defaultTheme="light"
              >
                <WalletProvider>
                  {getLayout(<Component {...pageProps} />)}
                  <SettingsButton />
                  <SettingsDrawer />
                  <ModalsContainer />
                  <DrawersContainer />
                </WalletProvider>
              </ThemeProvider>
            </Hydrate>
            <ReactQueryDevtools initialIsOpen={false} position="bottom-right" />
          </QueryClientProvider>
        </>
      </SessionProvider>
    </WagmiConfig>
  );
}

export default CustomApp;
