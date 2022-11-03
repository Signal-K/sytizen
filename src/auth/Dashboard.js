import React, { useContext } from 'react';
import { useHistory } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import { UserContext } from '../context/userContext';
import { logoutUser } from '../service/magic';

import Sidebar from '../components/SideBar Section/Sidebar';
import Body from '../components/Body Section/Body';

const Dashboard = () => {
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
    const { email } = useContext(UserContext);
    const history = useHistory();
    const handleLogOut = async () => {
        try {
            await logoutUser(); // Calls magic logout config
            history.replace('/');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className='p-2'>
            <div className='d-flex justify-content-end'>
                <Button variant="primary" onClick={handleLogOut}>
                    Sign Out
                </Button>
            </div>
            <h1 className='h1'>User: {email}</h1>
            <button onClick={handleLogOut}>Sign out</button>

            <div className='container'>
                <Sidebar />
                {/*<div className='App'>
                    <header className='App-header'>
                        <p>The current time is { currentTime }.</p>
                        <p>Planets: { planetTitle }.</p>
                    </header>
                </div> */}
                <Body />
            </div>
        </div>
    );
};

export default Dashboard;