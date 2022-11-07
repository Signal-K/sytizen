//import { useEffect, useState } from 'react';
//import { supabase } from '../lib/initSupabase';
import SignIn from './signin';
import styles from '../styles/home.module.css';

export default function Home() {
  return(
    <div className={styles.container}>
      {/*<SignIn />*/}
      <main className={styles.main}>
        <h1 className={styles.title}>
          Hello World
        </h1>
      </main>
    </div>
  )
}