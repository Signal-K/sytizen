import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';
import { Button, Form, FormGroup, FormLabel, FormControl } from 'react-bootstrap';

import Input from './input';

import logo from '../../Assets/logo-transparent.jpg';

// Magic imports
import { loginUser } from "../../service/magic";

const Container = styled.div`
  min-width: 400px;
  backdrop-filter: blur(35px);
  background-color: rgba(255, 255, 255, 0.8);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  padding: 0 2rem;

  @media (max-width: 900px) {
    width: 100vw;
    position: absolute;
    padding: 0;
  }
`

const LogoWrapper = styled.div`
  img {
    height: 6rem;
  }

  h3 {
    text-align: center;
    color: #ff8d8d;
    font-size: 22px;
  }

  span {
    color: #5dc399;
    font-weight: 300;
    font-size: 18px;
  }
`
/*
const Form = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  h3 {
    color: #666666;
    margin-bottom: 2rem;
  }

  button {
    width: 75%;
    max-width: 350px;
    min-width: 250px
    height: 40px;
    border: none;
    margin: 1rem 0;
    box-shadow: 0px 14px 9px -15px rgba(0, 0, 0, 0.25);
    border-radius: 8px;
    background-color: #79adeb;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease-in;

    &:hover {
      transform: translateY(-3px)
    }
  }
`
*/
const Sidebar = () => {
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
    <Container>
      <LogoWrapper>
        <img src={logo} alt="Signal Kinetics Logo" />
      </LogoWrapper>
      <h3>Star <span> Sailors </span> </h3>
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
    </Container>
  )
}

export default Sidebar