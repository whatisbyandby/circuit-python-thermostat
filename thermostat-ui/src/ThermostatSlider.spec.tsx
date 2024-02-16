import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import ThermostatSlider from './ThermostatSlider'

test('loads and displays greeting', async () => {
    // ARRANGE
    render(<ThermostatSlider mode={"heat"} max={95} min={45} targetTemperature={70} updateTargetTemperature={() => console.log('Test')} />)

    // ACT
    await userEvent.click(screen.getByText('Load Greeting'))
    await screen.findByRole('heading')

    // ASSERT
    expect(screen.getByRole('heading')).toHaveTextContent('hello there')
    expect(screen.getByRole('button')).toBeDisabled()
})