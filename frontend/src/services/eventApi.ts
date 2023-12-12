import axiosInstance from '../lib/axiosInstance';

export const createEvent = (data: EventApiRequest) => {
	return axiosInstance
		.post(`/event/`, data)
		.then(res => res.data)
		.catch(err => console.error(err));
};

export const findEventBySlug = (slug: string): Promise<EventApiResponse> => {
	return axiosInstance
		.get(`/event/${slug}/`)
		.then(res => res.data)
		.catch(err => console.error(err));
};

export default { createEvent };
