import './App.css'

import '@mantine/core/styles.css';

import { Container, MantineProvider } from '@mantine/core';
import Thermostat from './Thermostat';

function App() {

  return (
    <MantineProvider defaultColorScheme="dark">
      <Container>
        <Thermostat min={45} max={95} />
      </Container>
    </MantineProvider>
  )
}

export default App
