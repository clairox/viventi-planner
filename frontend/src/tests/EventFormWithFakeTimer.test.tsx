import { render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StepChanger } from './utils/StepChanger';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import { CreateEventPage } from '../pages/CreateEventPage';

jest.mock('react-datepicker/dist/react-datepicker.css', () => ({}));

const routes = [{ path: '/create', element: <CreateEventPage /> }];
const router = createMemoryRouter(routes, {
	initialEntries: ['/create'],
});

beforeAll(() => {
	jest.useFakeTimers({ advanceTimers: true }).setSystemTime(new Date('2020-01-01'));
});

afterAll(() => {
	jest.useRealTimers();
});

test.each([
	{ step: 1, name: 'Organizer Name', labelText: 'Your name *', expected: '' },
	{ step: 1, name: 'Organizer Email', labelText: 'Email *', expected: '' },
	{ step: 2, name: 'Event Name', labelText: 'Event name *', expected: '' },
	{ step: 2, name: 'Date', labelText: 'Date *', expected: '12/31/2019' },
	{ step: 2, name: 'Time', labelText: 'Time *', expected: '7:00 PM' },
	{ step: 2, name: 'Location', labelText: 'Location *', expected: '' },
	{ step: 3, name: 'Description', labelText: 'Tell us a little about your event *', expected: '' },
	{ step: 3, name: 'Event Capacity', labelText: 'Max number of attendees *', expected: '0' },
])("'$name' field has correct initial state", async ({ name, step, labelText, expected }) => {
	const { getByLabelText, getByText } = render(<RouterProvider router={router} />);
	const user = userEvent.setup();

	const sc = new StepChanger(user, getByLabelText, getByText);
	await sc.step(step);
	if (name === 'Location') await user.click(getByLabelText('In person'));

	expect((getByLabelText(labelText) as HTMLInputElement).value).toBe(expected);
});
