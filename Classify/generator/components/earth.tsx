import React from 'react';

export function Earth(props) {
    return (
        <>
            <ambientLight intensity={0.5} />
            <mesh>
                <sphereGeometry args={[1, 32, 32]} />
                <meshPhongMaterial color='red' />
            </mesh>
        </>,
    )
}