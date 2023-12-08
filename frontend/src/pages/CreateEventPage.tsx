import { Helmet } from 'react-helmet';
import { EventForm } from '../components/EventForm';

// TODO put event created at end of multi step form
export const CreateEventPage = () => {
	return (
		<section className="event-form">
			<Helmet>
				<title>Create an event</title>
				<meta name="description" content="Form for event creation." />
			</Helmet>
			<EventForm />
		</section>
	);
};
