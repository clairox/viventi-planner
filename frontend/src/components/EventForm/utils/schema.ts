import { z } from 'zod';

const schema = {
	organizerName: z.string().min(1, { message: 'Please provide your name' }).max(100, { message: 'Name should not exceed 100 characters' }),
	organizerEmail: z.string().email('Please enter a valid email address').min(1, { message: 'Email should not be empty' }).max(128, { message: 'Email should not exceed 128 characters' }),
	eventName: z.string().min(1, { message: 'Please enter the event name' }).max(50, { message: 'Event name should not exceed 50 characters' }),
	date: z
		.date({ required_error: 'Please select a date', invalid_type_error: 'Please select a date' })
		.min(new Date(new Date().setHours(0, 0, 0, 0)), { message: 'Event date should not be in the past' })
		.refine(date => date instanceof Date, { message: 'Please enter a valid date' }),
	time: z.date({ required_error: 'Please select a time', invalid_type_error: 'Please select a time' }).refine(time => time instanceof Date, { message: 'Please enter a valid time' }),
	description: z.string().min(1, { message: 'Please provide a description' }),
	maxCapacity: z.coerce.number().min(1, { message: 'Please specify a capacity of at least 1 person' }),
};

export const EventFormSchema = z.discriminatedUnion('eventFormat', [
	z.object({
		...schema,
		eventFormat: z.literal('virtual'),
		location: z.string(),
	}),
	z.object({
		...schema,
		eventFormat: z.literal('inPerson'),
		location: z.string().min(1, { message: 'Location required for in-person events' }),
	}),
]);

// TODO add timezone
