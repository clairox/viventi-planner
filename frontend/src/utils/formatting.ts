export const formatDateTime = (datetime: string): string => {
	return new Date(datetime).toLocaleString('en-us', {
		weekday: 'long',
		month: 'long',
		day: 'numeric',
		year: 'numeric',
		hour: 'numeric',
		minute: '2-digit',
		timeZoneName: 'short',
	});
};

export const formatLocation = (address: string, city: string, state: string, country: string): string => {
	return `${address}, ${city}, ${state}, ${country}`;
};
