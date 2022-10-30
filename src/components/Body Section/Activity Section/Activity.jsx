import React, { useState } from "react";
import './activity.css';

// Imported icons ====>
import { BsArrowRightShort } from 'react-icons/bs';

// Imported assets
import tesspic from '../../../Assets/StatElements/TessStat.png';
import Authenticate from "../../auth/Authenticate";
import { useHistory } from 'react-router-dom';
import { Button, Form, FormGroup, FormLabel, FormControl } from 'react-bootstrap';
import { loginUser } from "../../../service/magic";


const Activity = () => {
    // Magic/login form states
    const [email, setEmail] = useState('Initial Value');
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

    const handleChange = event => {
        setEmail(event.target.value);
      };

    return (
        <div className="activitySection">
            <input
                id="email"
                name="email"
                type="text"
                onChange={handleChange}
                value={email}
            />
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
            <div className="heading flex">
                <h1>Recent Activity</h1>
                <button className="btn flex">
                    See all activity <BsArrowRightShort />
                </button>
            </div>
            <div className="secContainer grid">
                <div className="singleCustomer flex">
                    <img src={tesspic} alt="Customer image" />
                    <div className="customerDetails">
                        <span className="name">Liam Arbuckle</span> {/* Static data - import from realtime supa later */}
                        <small>Ordered a new spaceship</small> {/* Ditto */}
                    </div>
                    <div className="duration">
                        2 min ago
                    </div>
                </div>
                <div className="singleCustomer flex">
                    <img src={tesspic} alt="Customer image" />
                    <div className="customerDetails">
                        <span className="name">Liam Arbuckle</span> {/* Static data - import from realtime supa later */}
                        <small>Ordered a new spaceship</small> {/* Ditto */}
                    </div>
                    <div className="duration">
                        2 min ago
                    </div>
                </div>
                <div className="singleCustomer flex">
                    <img src={tesspic} alt="Customer image" />
                    <div className="customerDetails">
                        <span className="name">Liam Arbuckle</span> {/* Static data - import from realtime supa later */}
                        <small>Ordered a new spaceship</small> {/* Ditto */}
                    </div>
                    <div className="duration">
                        2 min ago
                    </div>
                </div>
                <div className="singleCustomer flex">
                    <img src={tesspic} alt="Customer image" />
                    <div className="customerDetails">
                        <span className="name">Liam Arbuckle</span> {/* Static data - import from realtime supa later */}
                        <small>Ordered a new spaceship</small> {/* Ditto */}
                    </div>
                    <div className="duration">
                        2 min ago
                    </div>
                </div>
                <div className="singleCustomer flex">
                    <img src={tesspic} alt="Customer image" />
                    <div className="customerDetails">
                        <span className="name">Liam Arbuckle</span> {/* Static data - import from realtime supa later */}
                        <small>Ordered a new spaceship</small> {/* Ditto */}
                    </div>
                    <div className="duration">
                        2 min ago
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Activity;