import { getAllTimezones } from './timezones';

export const formatDateTime = (datetime: string, timezone: string): string => {
	datetime = (datetime + getAllTimezones().find(z => z.value === timezone)?.utcOffset).replace('T', ' ');

	return new Date(datetime).toLocaleString('en-us', {
		weekday: 'long',
		month: 'long',
		day: 'numeric',
		year: 'numeric',
		hour: 'numeric',
		minute: '2-digit',
		timeZoneName: 'short',
		timeZone: timezone,
	});
};

export const formatLocation = (address: string, city: string, state: string): string => {
	return `${address}, ${city}, ${state}`;
};
