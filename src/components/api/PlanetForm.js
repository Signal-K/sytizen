import React, {useState} from "react";
import { Button, Form, Input } from 'semantic-ui-react';

export const PlanetForm = () => {
    const [name, setName] = useState('');
    const [moons, setMoons] = useState(0);

    return (
        <Form>
            <Form.Field>
                <Input placeholder='planet title' value={name} onChange={ e => setName(e.target.value)} />
            </Form.Field>
            <Form.Field>
                <Input placeholder='planet moons' value={moons} onChange={ e => setMoons(e.target.value)} />
            </Form.Field>
            <Form.Field>
                <Button onClick={async () => {
                    const planet = {name, moons}; // Update this to match the properties in `./server/app.py` & in Supabase
                    const response = await fetch('/add_planet', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(planet),
                    });
                    if (response.ok) {
                        console.log('response worked');
                    }
                }}>
                    Submit
                </Button>
            </Form.Field>
        </Form>
    )
}