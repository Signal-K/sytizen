import Link from "next/link";
import React from "react";
import styles from '../styles/Header.module.css';
import SignInButton from "./SignInButton";

export default function Header () {
    return (
        <div className={styles.headerContainer}>
            <div>
                <Link href={'/'}>
                    <img src="/logo.png" alt='logo' />
                </Link>
            </div>
            <SignInButton />
        </div>
    )
}