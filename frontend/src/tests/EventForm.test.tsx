import { render, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { EventForm } from '../components/EventForm';
import { StepChanger } from './utils/StepChanger';

jest.mock('react-datepicker/dist/react-datepicker.css', () => ({}));

describe('next and back buttons work properly', () => {
	test('next button advances to next step', async () => {
		const { getByLabelText, getByText } = render(<EventForm />);
		const user = userEvent.setup();
		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(3);

		expect(getByText('Step 3 of 3')).toBeTruthy();
	});

	test('back button returns to previous step', async () => {
		const { getByLabelText, getByText } = render(<EventForm />);
		const user = userEvent.setup();
		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(3);

		await user.click(getByText('Back'));
		expect(getByText('Step 2 of 3')).toBeTruthy();

		await user.click(getByText('Back'));
		expect(getByText('Step 1 of 3')).toBeTruthy();
	});

	test('back button does not exist on first page', () => {
		const { queryByText } = render(<EventForm />);

		expect(queryByText('Back')).toBeNull();
	});

	test('next button does not exist on last page', async () => {
		const { getByLabelText, getByText, queryByText } = render(<EventForm />);
		const user = userEvent.setup();
		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(3);

		expect(queryByText('Next')).toBeNull();
	});
});

describe('location field only shown when format is in person', () => {
	test('location input hidden when format is virtual', async () => {
		const { getByLabelText, getByText, queryByLabelText } = render(<EventForm />);
		const user = userEvent.setup();

		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(2);
		await user.click(getByLabelText('Virtual'));

		expect(queryByLabelText('Location *')).toBeNull();
	});

	test('location input shows when format is in person', async () => {
		const { getByLabelText, getByText, queryByLabelText } = render(<EventForm />);
		const user = userEvent.setup();

		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(2);
		await user.click(getByLabelText('In person'));

		expect(queryByLabelText('Location *')).not.toBeNull();
	});

	test('location is empty when format is virtual', async () => {
		const { getByLabelText, getByText } = render(<EventForm />);
		const user = userEvent.setup();

		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(2);
		await user.click(getByLabelText('In person'));

		const inputField = getByLabelText('Location *') as HTMLInputElement;

		await user.type(inputField, 'Test Location');
		await user.click(getByLabelText('Virtual'));

		await waitFor(() => {
			expect(inputField.value).toBe('');
		});
	});
});

describe('user input', () => {
	test.each([
		{ step: 1, name: 'Organizer Name', labelText: 'Your name *', expected: 'Test User' },
		{ step: 1, name: 'Organizer Email', labelText: 'Email *', expected: 'test@test.com' },
		{ step: 2, name: 'Event Name', labelText: 'Event name *', expected: 'Test Event' },
		{ step: 2, name: 'Date', labelText: 'Date *', expected: '6/3/2078' },
		{ step: 2, name: 'Time', labelText: 'Time *', expected: '1:00 AM' },
		{ step: 2, name: 'Location', labelText: 'Location *', expected: 'Test Location' },
		{
			step: 3,
			name: 'Description',
			labelText: 'Tell us a little about your event *',
			expected: 'Test Description',
		},
		{ step: 3, name: 'Event Capacity', labelText: 'Max number of attendees *', expected: '10' },
	])("user can type into '$name' field", async ({ name, step, labelText, expected }) => {
		const { getByLabelText, getByText } = render(<EventForm />);
		const user = userEvent.setup();

		const sc = new StepChanger(user, getByLabelText, getByText);
		await sc.step(step);
		if (name === 'Location') await user.click(getByLabelText('In person'));

		const inputField = getByLabelText(labelText) as HTMLInputElement;

		await user.clear(inputField);
		await user.type(inputField, expected);

		expect(inputField.value).toBe(expected);
	});

	const tooLongString = 'x'.repeat(200);
	const tooLongEmail = tooLongString + '@test.com';

	test.each([
		{
			step: 1,
			name: 'Organizer Name',
			labelText: 'Your name *',
			value: '',
			expectedError: 'Please provide your name',
		},
		{
			step: 1,
			name: 'Organizer Name',
			labelText: 'Your name *',
			value: tooLongString,
			expectedError: 'Name should not exceed 100 characters',
		},
		{
			step: 1,
			name: 'Organizer Email',
			labelText: 'Email *',
			value: '',
			expectedError: 'Please enter a valid email address',
		},
		{
			step: 1,
			name: 'Organizer Email',
			labelText: 'Email *',
			value: tooLongEmail,
			expectedError: 'Email should not exceed 128 characters',
		},
		{
			step: 2,
			name: 'Event Name',
			labelText: 'Event name *',
			value: '',
			expectedError: 'Please enter the event name',
		},
		{
			step: 2,
			name: 'Event Name',
			labelText: 'Event name *',
			value: tooLongString,
			expectedError: 'Event name should not exceed 50 characters',
		},
		{ step: 2, name: 'Date', labelText: 'Date *', value: '', expectedError: 'Please select a date' },
		{ step: 2, name: 'Time', labelText: 'Time *', value: '', expectedError: 'Please select a time' },
		{
			step: 2,
			name: 'Location',
			labelText: 'Location *',
			value: '',
			expectedError: 'Location required for in-person events',
		},
		{
			step: 3,
			name: 'Description',
			labelText: 'Tell us a little about your event *',
			value: '',
			expectedError: 'Please provide a description',
		},
		{
			step: 3,
			name: 'Event Capacity',
			labelText: 'Max number of attendees *',
			value: '',
			expectedError: 'Please specify a capacity of at least 1 person',
		},
		{
			step: 3,
			name: 'Event Capacity',
			labelText: 'Max number of attendees *',
			value: '0',
			expectedError: 'Please specify a capacity of at least 1 person',
		},
	])(
		"'$expectedError' displayed if '$value' in '$name' field",
		async ({ name, step, labelText, value, expectedError }) => {
			const { getByLabelText, getByText } = render(<EventForm />);
			const user = userEvent.setup();

			const sc = new StepChanger(user, getByLabelText, getByText);
			await sc.step(step);
			if (name === 'Location') await user.click(getByLabelText('In person'));

			const inputField = getByLabelText(labelText) as HTMLInputElement;

			await user.clear(inputField);
			if (value) await user.type(inputField, value);

			if (step === 3) {
				await user.click(getByText('Finish'));
			} else {
				await user.click(getByText('Next'));
			}

			expect(getByText(expectedError)).not.toBeNull();
		}
	);
});
