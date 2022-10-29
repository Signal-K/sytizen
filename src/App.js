import React, { useState, useEffect, useContext } from 'react';
import './App.css';

import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
//import SignIn from './pages/Signin';

/* Eth Providers
import { createClient, configureChains, defaultChains, WagmiConfig } from 'wagmi';
import { publicProvider } from 'wagmi/providers/public';
import { SessionProvider } from 'next-auth/react'; */

// Sass components
import Body from './components/Body Section/Body';

// Menu components
import Sidebar from './components/SideBar Section/Sidebar';

// Magic
import { magic } from './lib/magic';
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import { UserContext } from "./lib/UserContext";

// Magic UI components
import Layout from './components/layout';
import PaymentForm from './components/payment-form';
import Payment from './components/payment';
import Login from './components/login';

// Magic promises
const promise = loadStripe("pk_test_51L1UB5EXgarheYLkmZE9jqvsPe0d5UjoH2aZJvrIv6W55J0HEsQHE6wmJtXRSRMI4GulhzAetAxQE1yiVi2XvYVO00khAvACG1");

/* If isLoggedIn is true, set the UserContext with user data -> Otherwise, set it to {user: null}
useEffect(() => {
    setUser({ loading: true });
    magic.user.isLoggedIn().then(isLoggedIn => {
      return isLoggedIn ? magic.user.getMetadata().then(userData => setUser(userData)) : setUser({ user: null });
    });
}, []);  */

function App() {
    /*const [currentTime, setCurrentTime] = useState(0);
    const [planetTitle, setPlanetTitle] = useState('')

    // Pull content from Flask API
    useEffect(() => {
        fetch('/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        });
    }, [])

    // Fetch planets from Flask API
    useEffect(() => {
        fetch('/planets').then(res => res.json()).then(data => {
            setPlanetTitle(data.title);
        });
    }, [])*/
    // Create a hook to check whether or not user has lifetime acess
    const [lifetimeAccess, setLifetimeAccess] = useState(false);
    // Create a hook to prevent infinite loop in useEffect inside of /components/premium-content
    const [
        lifetimeAccessRequestStatus,
        setLifetimeAccessRequestStatus,
    ] = useState("");
    // Create a hook to help us determine whether or not the  user is logged in
    const [user, setUser] = useState();
    
    // If isLoggedIn is true, set the UserContext with user data
    // Otherwise, set it to {user: null}
    useEffect(() => {
        setUser({ loading: true });
        magic.user.isLoggedIn().then((isLoggedIn) => {
        return isLoggedIn
            ? magic.user.getMetadata().then((userData) => setUser(userData))
            : setUser({ user: null });
        });
    }, []);

    <Router>
        <Switch>
            <UserContext.Provider value={[user, setUser]}>
                <Layout>
                    <Route path="/" exact component={App} />
                    <Route path="/login" component={Login} />
                    <Route path="/profile" component={Profile} />
                    <Route path="/callback" component={Callback} />
                </Layout>
            </UserContext.Provider>
        </Switch>
    </Router>

    return (
        /*<div className='App'>
            <header className='App-header'>
                <p>The current time is { currentTime }.</p>
                <p>Planets: { planetTitle }.</p>
            </header>
        </div> */
        <div className='container'>
            <Sidebar />
            <Body />
        </div>
    );
}

export default App;