import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import { Button, Form, FormGroup, FormLabel, FormControl } from 'react-bootstrap';
import { loginUser } from "../service/magic";
import Login from "../pages/Login";

const Authenticate = () => {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState('');
    const [error, setError] = useState(null);
    const history = useHistory();
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        if (!email) {
            setLoading(false);
            setError('Email is invalid');
            return;
        } try {
            await loginUser(email);
            setLoading(false);
            history.replace('/dashboard');
        } catch (error) {
            setError('Unable to log in');
            console.error(error);
        }
    };

    const handleChange = (event) => {
        setEmail(event.target.value);
    };

    return (
        <div className="w-50 p-5 mt-5 mx-auto">
            <h1 className="h1 text-center">Magical login form</h1>
            <Form onSubmit={handleSubmit} className='p-2 my-5 mx-auto'>
                <FormGroup className="mt-3">
                    <FormLabel fontSize="sm">Enter Email Address</FormLabel>
                    <FormControl
                        type="email"
                        name="email"
                        id="email"
                        value={email}
                        onChange={handleChange}
                        placeholder="Email Address"
                    />
                </FormGroup>
            </Form>
            <Login />
        </div>
    );
};

export default Authenticate;