import React from "react";
import { useState } from "react";
import axios from "axios";

function PostForm() {
    const url = ""
    const [data, setData] = useState({
        name: "",
        iduser: ""
    })

    function submit(e) {
        e.preventDefault();
        axios.post(url, {
            name: data.name,
            iduser: date.iduser
        })
        .then(res => {
            console.log(res.data)
        })
    }

    function handle(e) {
        const newdata = { ...data }
        newdata[e.target.id] = e.target.value
        setData(newdata)
        console.log(newdata)
    }

    return (
        <div>
            <form onSubmit={(e) => SubmitEvent(e)}>
                <input onChange={(e) => handle(e)} value={data.name} placeholder="name" type="text"></input>
                <input onChange={(e) => handle(e)} value={data.iduser} placeholder="iduser" type="number"></input>
            </form>
            <button>Submit</button>
        </div>
    )
}

export default PostForm;