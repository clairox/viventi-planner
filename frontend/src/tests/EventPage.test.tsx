import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import { findEventBySlug } from '../services/eventApi';
import { render, waitFor } from '@testing-library/react';
import { EventPage } from '../pages/EventPage';

jest.mock('../services/eventApi', () => {
	const event = {
		event_id: 1,
		event_name: 'Test Event',
		date: '2050-01-01',
		time: '06:00:00',
		tz_name: 'America/New_York',
		event_datetime: '2050-01-01T06:00:00',
		location_name: 'Test Location',
		location_address: '22 Location Lane',
		location_city: 'Test',
		location_state: 'State',
		location_country: 'Fake Country',
		location_zip: '10001',
		organizer_name: 'John Doe',
		organizer_email: 'johndoe@test.com',
		event_max_capacity: 50,
		event_format: 'in-person',
		description: 'Test Description',
		status: 'verified',
		verified: true,
		created_at: '2049-12-01T01:00:00Z',
		modified_at: '2049-12-01T01:00:00Z',
	};
	return {
		findEventBySlug: jest.fn(() => Promise.resolve(event)),
	};
});

const routes = [{ path: '/event/:eventSlug', element: <EventPage /> }];
const router = createMemoryRouter(routes, {
	initialEntries: ['/event/testSlug'],
});

test('event data renders correctly', async () => {
	const { queryByText } = render(<RouterProvider router={router} />);

	await waitFor(() => expect(findEventBySlug).toHaveBeenCalled());

	expect(queryByText('Test Event')).not.toBeNull();
	expect(queryByText('When: Saturday, January 1, 2050 at 6:00 AM EST')).not.toBeNull();
	expect(queryByText('Test Location')).not.toBeNull();
	expect(queryByText('22 Location Lane, Test, State')).not.toBeNull();
	expect(queryByText('When: Saturday, January 1, 2050 at 6:00 AM EST')).not.toBeNull();
	expect(queryByText('Organized by: John Doe')).not.toBeNull();
	expect(queryByText('Test Description')).not.toBeNull();
});
test.skip('date is formatted correctly based on date formats and time zones', async () => {});
test.skip('location is not present if format is virtal', () => {});
test.skip('location is not present if format is virtal', () => {});
test.skip('location formatted correctly based on location', () => {});
