import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';
import { useParams } from 'react-router-dom';
import { findEventBySlug } from '../services/eventApi';

export const EventPage = () => {
	const { eventSlug } = useParams();
	const [eventData, setEventData] = useState<EventApiResponse | null>(null);

	useEffect(() => {
		if (eventSlug) {
			findEventBySlug(eventSlug).then(data => {
				setEventData(data);
				console.log(data);
			});
		}
	}, [eventSlug]);

	const renderEventData = () => {
		if (!eventData) return;

		const {
			event_name,
			date,
			time,
			location_name,
			location_address,
			location_city,
			location_state,
			location_country,
			location_zip,
			organizer_name,
			event_format,
			event_max_capacity,
			description,
		} = eventData;

		const location = location_address
			? `${location_address}, ${location_city}, ${location_state}, ${location_country} ${location_zip}`
			: '';

		return (
			<>
				<h1>{event_name}</h1>
				<div>
					Time: {date} {time}
				</div>
				<div>Format: {event_format === 'virtual' ? 'Virtual' : 'In person'}</div>
				{location ? <div>Location: {(location_name + ', ' || '') + location}</div> : <></>}
				<div>Organized by: {organizer_name}</div>
				<div>Capacity: {event_max_capacity}</div>
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
