import type { NextPage } from "next";
import Head from "next/head";
import React from "react";

// Supa data
import { createClient } from "@supabase/supabase-js";
//export const Supabase = createClient(supabaseUrl, supabaseKey);

const CommentsHome: NextPage = () => {
    return (
        <div>
          <Head>
            <title>Comments Page</title>
          </Head>
                <div className="pt-36 flex justify-center">
            <div className="min-w-[600px]">
              <h1 className="text-4xl font-bold ">Comments</h1>
              <form onSubmit={onSubmit} className="mt-8 flex gap-8">
                <input type="text" placeholder="Add a comment" className="p-2 border-b focus:border-b-gray-700 w-full outline-none" />
                <button className="px-4 py-2 bg-green-500 rounded-lg text-white">Submit</button>
              </form>
            </div>
          </div>
        </div>
    );
};

export default CommentsHome;