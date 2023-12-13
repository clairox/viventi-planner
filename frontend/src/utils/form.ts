const sanitizeFormData = (data: EventFormData): SanitizedEventFormData => {
	const { date, time, ...rest } = data;

	const month = (date.getMonth() + 1).toString().padStart(2, '0');
	const _date = date.getDate().toString().padStart(2, '0');
	const year = date.getFullYear();
	const dateWithoutTime = `${year}-${month}-${_date}`;

	const hours = time.getHours();
	const minutes = time.getMinutes().toString().padStart(2, '0');

	const timeWithoutDate = `${hours}:${minutes}:00`;

	return {
		...rest,
		date: dateWithoutTime,
		time: timeWithoutDate,
	};
};

export { sanitizeFormData };
