import React from "react";
import styled from "styled-components";
import { Container } from "react-dom";

// Asset imports
import bgImg from '../Assets/Pages/bg.png';

// Component imports
import Sidebar from "../components/auth/home/Sidebar";
import main from "../components/auth/home/main";

const Login = () => {
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
    `

    return (
        <Container>
            <Wrapper>
                <h1>Test</h1>
            </Wrapper>
        </Container>
    );
};

export default Login;