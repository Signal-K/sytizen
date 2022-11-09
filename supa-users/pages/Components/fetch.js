import React, { useEffect, useState } from 'react';

function fetch() {
    const [todos, setTodos] = useState([]);

    useEffect(() => {
        fetch("/todos").then(response => 
        })
    })
}