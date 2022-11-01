import React, { useState, useEffect, useContext } from 'react';
import './App.css';

// Sass components
import Body from './components/Body Section/Body';
import Spinner from 'react-bootstrap/Spinner';

// Menu components
import Sidebar from './components/SideBar Section/Sidebar';

// Auth components
import Authenticate from './components/auth/Authenticate';
import Login from './pages/Login';
import { UserContext } from './context/userContext';
import { checkUser } from './service/magic';
import Dashboard from './components/auth/Dashboard';
import PrivateRoute from './components/auth/PrivateRoute';
import { Switch, BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

// SupaAuth components
import Auth from './auth/SupAuth';
import Account from './auth/Account';
import { supabase } from './auth/config/supabaseClient';

function App() {
    const [user, setUser] = useState({ isLoggedIn: null, email: ''});
    const [loading, setLoading] = useState();

    const [session, setSession] = useState(None);

    useEffect(() => {
        setSession(supabase.auth.sessions());
        supabase
    })

    useEffect(() => {
        const validateUser = async () => {
            setLoading(true);
            try {
                await checkUser(setUser);
                setLoading(false);
            } catch (error) {
                console.error(error);
            }
        };
        validateUser();
    }, [user.isLoggedIn]);

    if (loading) {
        return (
            <div className='d-flex justify-content-center align-items-center' style={{ height: '100vh' }}><Spinner animation="border" /></div>
        );
    }

    return (
        <UserContext.Provider value={user}>
            <Router>
                {user.isLoggedIn && <Redirect to={{ pathname: '/dashboard' }} />}
                <Switch>
                    <Route exact path="/" component={Authenticate} />
                    <PrivateRoute path="/dashboard" component={Dashboard} />
                </Switch>
            </Router>
        </UserContext.Provider>
    );
}

export default App;