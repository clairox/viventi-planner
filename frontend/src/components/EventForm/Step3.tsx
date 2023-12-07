import React from 'react';

import { useFormContext } from 'react-hook-form';
import { EventFormSchemaType } from './types/schema';

type Props = {
	prevStep: () => void;
};

export const Step3: React.FunctionComponent<Props> = ({ prevStep }) => {
	const {
		register,
		formState: { errors },
	} = useFormContext<EventFormSchemaType>();

	return (
		<>
			<div className="form-group">
				<label htmlFor="description">Tell us a little about your event *</label>
				<textarea id="description" {...register('description', { required: true })} aria-required="true" />
				{errors.description && <span>{errors.description.message}</span>}
			</div>
			<div className="form-group">
				<label htmlFor="maxCapacity">Max number of attendees *</label>
				<input type="text" id="maxCapacity" {...register('maxCapacity', { required: true })} aria-required="true" />
				{errors.maxCapacity && <span>{errors.maxCapacity.message}</span>}
			</div>
			<button onClick={prevStep}>Back</button>
			<button type="submit">Finish</button>
		</>
	);
};
