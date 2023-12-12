import { useParams, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { verifyEvent } from '../services/verificationApi';

export const VerificationRedirect = () => {
	const { token } = useParams();
	const [content, setContent] = useState(<></>);

	useEffect(() => {
		if (token) {
			verifyEvent(token)
				.then(data => {
					const { event_slug, edit_token } = data;
					setContent(
						<Navigate
							to={{ pathname: `/event/${event_slug}/links` }}
							state={{ token: edit_token }}
							replace
						/>
					);
				})
				.catch(err => {
					if (err.response.status === 401) {
						// TODO redirect to page which tells user verification token expired, send new one
					} else if (err.response.status === 404) {
						// TODO redirect to page which tells user event does not exist, make new one
					} else if (err.response.status === 409) {
						// TODO redirect to event page
					} else {
						// TODO redirect to error page for given status code
					}
				});
		}
	}, [token]);

	return content;
};
