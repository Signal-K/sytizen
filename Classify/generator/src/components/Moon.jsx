import React, { useRef } from 'react';
import EarthDayMap from '../textures/earth_daymap.jpeg';
import EarthNormalMap from '../textures/earth_normal_map.jpeg';
import EarthSpecularMap from '../textures/earth_specular_map.jpeg';
import EarthNightMap from '../textures/earth_nightmap.jpeg';
import EarthCloudsMap from '../textures/earth_clouds.jpeg';
import { TextureLoader, geLight } from 'three';
import { useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';

export function Moon(props) {

    return (
        <>
            <pointLight color="#f6f3ea" position={[2, 0, 5]} intensity={1.2} /> {/* Make the colour of the sun slightly yellowed, by the earth's atmosphere */}
            <Stars radius={300} depth={60} count={20000} factor={7} saturation={0} fade={true} />
            <mesh>
                <sphereGeometry args={[1.005, 32, 32]} />
            </mesh>
            <mesh>
                <sphereGeometry args={[1, 32, 32]} />
                <OrbitControls enableZoom={true} enablePan={true} enableRotate={true} zoomSpeed={0.6} panSpeed={0.5} rotateSpeed={0.4} />
            </mesh>
        </>
    )
}