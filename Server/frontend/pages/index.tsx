import type { NextPage } from "next";
import useAuthenticate from '../hooks/useAuthenticate';
import { useAddress, useDisconnect, useUser, useLogin, useLogout, useMetamask } from "@thirdweb-dev/react";
import { useEffect, useState } from "react";
import { PublicationSortCriteria, useExplorePublicationsQuery } from "../graphql/generated";

export default function Home () {
  const { data, isLoading, error } = useExplorePublicationsQuery({
    request: {
      sortCriteria: PublicationSortCriteria.TopCollected,
    },
  });

  return (
    <div>Hello World</div>
  );
};