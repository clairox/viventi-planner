import axios from 'axios';

const baseURL = process.env.API_PATH;
const axiosInstance = axios.create({ baseURL });

axiosInstance.interceptors.response.use(
	res => res,
	err => {
		if (err.response.status === 409) return err;

		switch (err.response.status) {
			case 400:
				window.location.href = '/400';
				break;
			case 404:
				window.location.href = '/404';
				break;
			case 500:
				window.location.href = '/500';
				break;
			default:
				break;
		}
		return Promise.reject(err);
	}
);

export default axiosInstance;
