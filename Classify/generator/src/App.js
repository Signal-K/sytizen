import styled from 'styled-components';
import { Canvas } from '@react-three/fiber';
//import { Suspense } from 'react';
// import { Earth } from './components/Earth';
// import { Moon } from './components/Moon';
import Planet from '@xaroth8088/react-planet';
// import { ThreeScene } from './components/SceneRenderer';
import './index.css'

const CanvasContainer = styled.div`
  width: 100%;
  height: 100%;
`;


function App () {
  return (
    <CanvasContainer>
      {/*<Canvas>
        <Suspense fallback={null}>
          <Earth />
        </Suspense>
      </Canvas> */}
      <Canvas>
        <Planet />
      </Canvas>
    </CanvasContainer>
  )
}

export default App;