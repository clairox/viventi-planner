import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';
import { useParams } from 'react-router-dom';
import { findEventBySlug } from '../services/eventApi';
import { formatDateTime, formatLocation } from '../utils/formatting';

export const EventPage = () => {
	const { eventSlug } = useParams();
	const [eventData, setEventData] = useState<EventApiResponse | null>(null);

	useEffect(() => {
		if (eventSlug) {
			findEventBySlug(eventSlug).then(data => {
				setEventData(data);
			});
		}
	}, [eventSlug]);

	const renderEventData = () => {
		if (!eventData) return;

		const {
			event_name,
			event_datetime,
			location_name,
			location_address,
			location_city,
			location_state,
			location_country,
			organizer_name,
			event_format,
			description,
		} = eventData;

		const datetime = formatDateTime(event_datetime);
		const location =
			location_address && location_city && location_state && location_country
				? formatLocation(location_address, location_city, location_state, location_country)
				: '';

		return (
			<>
				<h1>{event_name}</h1>
				<div>When: {datetime}</div>
				{event_format === 'in-person' ? (
					<div>
						Where: <div style={{ fontWeight: 600 }}>{location_name || location_address}</div>{' '}
						<div>{location}</div>
					</div>
				) : (
					<></>
				)}
				<div>Organized by: {organizer_name}</div>
				<p>{description}</p>
			</>
		);
	};

	return (
		<>
			<Helmet>
				<title>Event</title>
				<meta name="description" content="Details about event." />
			</Helmet>
			<div>{renderEventData()}</div>
		</>
	);
};
