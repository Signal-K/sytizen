import type { NextPage } from "next";
import useAuthenticate from '../hooks/useAuthenticate';
import { useAddress, useDisconnect, useUser, useLogout, useMetamask, ConnectWallet } from "@thirdweb-dev/react";
import { useEffect, useState } from "react";
import { PublicationSortCriteria, useExplorePublicationsQuery } from "../graphql/generated";
import useLogin from "../lib/auth/useLogin";
import SignInButton from "../components/SignInButton";

export default function Home () {
  return <SignInButton />;
};