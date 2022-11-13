import type { GetStaticProps, InferGetStaticPropsType } from 'next';
import { NextSeo } from 'next-seo';
import type { NextPageWithLayout } from '@/types';
import DashboardLayout from '@/layouts/_dashboard';
import CoinSlider from '@/components/ui/coin-card';
import OverviewChart from '@/components/ui/chats/overview-chart';
import LiquidityChart from '@/components/ui/chats/liquidity-chart';
import VolumeChart from '@/components/ui/chats/volume-chart';
import TopPools from '@/components/ui/top-pools';
import TransactionTable from '@/components/transaction/transaction-table';
import TopCurrencyTable from '@/components/top-currency/currency-table';
import { coinSlideData } from '@/data/static/coin-slide-data';
import Avatar from '@/components/ui/avatar';
import TopupButton from '@/components/ui/topup-button';
//images
import AuthorImage from '@/assets/images/author.jpg';

import SignIn from "./auth/Signin";
import { useEffect, useState } from 'react';
import { supabase } from './api/auth/supabaseClient';

export const getStaticProps: GetStaticProps = async () => {
  return {
    props: {},
  };
};

const HomePage: NextPageWithLayout<
  InferGetStaticPropsType<typeof getStaticProps>
> = () => {
  return (
    <SignIn />
  );
};

HomePage.getLayout = function getLayout(page) {
  /*const [session, setSession] = useState(null);
  
  useEffect(() => {
      setSession(supabase.auth.session());

      supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      });
  }, []);*/
  
  return <DashboardLayout>{page}</DashboardLayout>;
};

export default HomePage;
