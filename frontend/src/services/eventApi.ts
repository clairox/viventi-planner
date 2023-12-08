import { EventFormSchemaType } from '../components/EventForm/types/schema';
import axiosInstance from '../lib/axiosInstance';

const sanitizeFormData = (data: EventFormSchemaType) => {
	const { date, time, ...rest } = data;

	const month = (date.getMonth() + 1).toString().padStart(2, '0');
	const _date = date.getDate().toString().padStart(2, '0');
	const year = date.getFullYear();
	const dateWithoutTime = `${year}-${month}-${_date}`;

	const hours = date.getHours();
	const minutes = time.getMinutes().toString().padStart(2, '0');

	const timeWithoutDate = `${hours}:${minutes}:00`;

	return {
		...rest,
		date: dateWithoutTime,
		time: timeWithoutDate,
	};
};

export const createEvent = async (data: EventFormSchemaType) => {
	const { date, time } = sanitizeFormData(data);

	return await axiosInstance
		.post('/event/', {
			event_name: data.eventName,
			date: date,
			time: time,
			event_format: data.eventFormat === 'inPerson' ? 'in-person' : 'virtual',
			location_name: data.location,
			location_address: data.location,
			location_city: data.location,
			location_state: data.location,
			location_country: data.location,
			location_zip: '10001',
			organizer_name: data.organizerName,
			organizer_email: data.organizerEmail,
			event_max_capacity: data.maxCapacity,
			description: data.description,
		})
		.then(res => res.data)
		.catch(err => console.log(err));
};

export default { createEvent };
