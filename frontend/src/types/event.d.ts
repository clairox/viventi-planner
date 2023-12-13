type EventFormat = 'virtual' | 'in-person';
type EventStatus = 'inactive' | 'verified' | 'canceled' | 'completed';

type EventApiRequest = {
	event_name: string;
	date: string;
	time: string;
	tz_name: string;
	location_name: string | undefined;
	location_address: string | undefined;
	location_city: string | undefined;
	location_state: string | undefined;
	location_country: string | undefined;
	location_zip: string | undefined;
	organizer_name: string;
	organizer_email: string;
	event_max_capacity: number;
	event_format: EventFormat;
	description: string;
};

type EventApiResponse = {
	event_id: number;
	event_name: string;
	date: string;
	time: string;
	event_datetime: string;
	tz_name: string;
	location_name: string | undefined;
	location_address: string | undefined;
	location_city: string | undefined;
	location_state: string | undefined;
	location_country: string | undefined;
	location_zip: string | undefined;
	organizer_name: string;
	organizer_email: string;
	event_max_capacity: number;
	event_format: EventFormat;
	description: string;
	status: EventStatus;
	verified: boolean;
	created_at: string;
	modified_at: string;
};

type EventFormData = {
	eventName: string;
	date: Date;
	time: Date;
	timezone: { value: string; label: string };
	location: string | undefined;
	// locationName: string | undefined;
	// locationAddress: string | undefined;
	// locationCity: string | undefined;
	// locationState: string | undefined;
	// locationCountry: string | undefined;
	// locationZip: string | undefined;
	organizerName: string;
	organizerEmail: string;
	maxCapacity: number;
	eventFormat: 'virtual' | 'inPerson';
	description: string;
};

type SanitizedEventFormData = {
	eventName: string;
	date: string;
	time: string;
	timezone: { value: string; label: string };
	location: string | undefined;
	// locationName: string | undefined;
	// locationAddress: string | undefined;
	// locationCity: string | undefined;
	// locationState: string | undefined;
	// locationCountry: string | undefined;
	// locationZip: string | undefined;
	organizerName: string;
	organizerEmail: string;
	maxCapacity: number;
	eventFormat: 'virtual' | 'inPerson';
	description: string;
};
