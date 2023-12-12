import axios from 'axios';

export const verifyEvent = (token: string): Promise<EventVerificationApiResponse> => {
	return axios
		.post(`${process.env.API_PATH}/verify-event/${token}/`)
		.then(res => res.data)
		.catch(err => {
			throw err;
		});
};
