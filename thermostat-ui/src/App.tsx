import { useState } from 'react'

import './App.css'

import '@mantine/core/styles.css';

import { Container, MantineProvider } from '@mantine/core';
import ThermostatSlider from './ThermostatSlider'
import WebsocketComponent from './WebsocketComponent';

function App() {

  return (
    <MantineProvider defaultColorScheme="dark">
      <Container>
        <WebsocketComponent />
      </Container>
    </MantineProvider>
  )
}

export default App
