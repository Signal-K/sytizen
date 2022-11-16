import React from "react";
import { List, Header, Rating } from "semantic-ui-react";

export const Planets = ({ planets }) => {
    return (
        <List>
            {planets.map(planet => {
                return (
                    <List.Item key={planet.name}>
                        <Header>{planet.name}</Header>
                        <br />
                        <Header>Moons: {planet.moons}</Header>
                        <Rating rating={planet.moons} maxRating='5' disabled/>
                        <br />
                        <br />
                    </List.Item>
                )
            })}
        </List>
    )
}