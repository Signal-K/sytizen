import React, { useState, useEffect, useContext } from 'react';
import './App.css';

// Sass components
import Body from './components/Body Section/Body';
import Spinner from 'react-bootstrap/Spinner';

// Menu components
import Sidebar from './components/SideBar Section/Sidebar';

/* SupaAuth components */
import SupabaseAuth from './pages/Authenticate';
/*import Auth from './components/auth/SupAuth';
import SignIn from './pages/Signin';
import Account from './components/auth/Account';
import { supabase } from './components/auth/config/supabaseClient'; */

function App() {
    const [user, setUser] = useState({ isLoggedIn: null, email: ''});
    const [loading, setLoading] = useState();

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
                    <Route exact path="/" component={SupabaseAuth} />
                    <PrivateRoute path="/dashboard" component={Dashboard} />
                </Switch>
            </Router>
        </UserContext.Provider>
    );
}

export default App;