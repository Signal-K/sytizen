import React, { useState } from "react";
import styled from "styled-components";
import { Container } from "react-dom";
import { useHistory } from 'react-router-dom';

// Asset imports
import bgImg from '../Assets/Pages/bg.png';

// Component imports
import Sidebar from "../components/auth/home/Sidebar";
import Main from "../components/auth/home/Main";

// Magic imports
import { loginUser } from "../service/magic";

const Login = () => {
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

    const Container = styled.div`
        background: #eefcff;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
    `;

    const Wrapper = styled.div`
        background-image: url(${bgImg});
        background-position: center;
        background-size: cover;
        background-repeat: no-repeat;
        width: 100%;
        height: 100%;
        display: flex;
    `

    return (
        <Container>
            <Wrapper>
                <Sidebar />
                <Main />
            </Wrapper>
        </Container>
    );
};

export default Login;