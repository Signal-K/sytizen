import React, { useContext } from 'react';
import { useHistory } from 'react-router-dom';
import { Button } from 'react-bootstrap/Button';

import Sidebar from './components/backend/Body Section/SideBar Section/Sidebar';
import Body from './components/backend/Body Section/Body';

const Dashboard = () => {
    return (
        <div className='p-2'>
            <div className='d-flex justify-content-end'>
                
            </div>
            <div className='container'>
                <Sidebar />
                <Body />
            </div>
        </div>
    )
}

export default Dashboard;