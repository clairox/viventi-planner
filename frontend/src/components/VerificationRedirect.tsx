import axios from 'axios';
import { useParams, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export const VerificationRedirect = () => {
	const { token } = useParams();
	const [content, setContent] = useState(<></>);

	useEffect(() => {
		axios
			.post(`${import.meta.env.VITE_API_URL}/verify-event/${token}/`)
			.then(res => {
				console.log(res.data);
				const { event_slug, edit_token } = res.data;
				setContent(<Navigate to={{ pathname: `/event/${event_slug}/links` }} state={{ token: edit_token }} replace />);
			})
			.catch(() => {});
	});

	return content;
};
