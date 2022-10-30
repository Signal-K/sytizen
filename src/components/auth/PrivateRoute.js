import React, { Component, useContext } from 'react';
import { Redirect, Route } from 'react-router-dom';
import { UserContext } from '../../context/userContext';

const PrivateRoute = ({ component: Component, ...rest }) => {
    const { isLoggedIn } = useContext(UserContext); // Call context to check state/us of user through magic sdk

    return (
        <Route
            {...rest}
            render={(props) =>
            isLoggedIn ? <Component {...props} /> : <Redirect to="/" />
            }
        />
    );
};

export default PrivateRoute;

/*
1. Check user login status
Render component if true
2. Redirect to auth page if not true
*/