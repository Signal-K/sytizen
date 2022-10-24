import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [currentTime, setCurrentTime] = useState(0);
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
    }, [])

    return (
        <div className='App'>
            <header className='App-header'>
                <p>The current time is { currentTime }.</p>
                <p>Planets: { planetTitle }.</p>
            </header>
        </div>
    );
}

export default App;