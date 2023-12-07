import React from 'react';
import { useFormContext } from 'react-hook-form';
import { EventFormSchemaKey, EventFormSchemaType } from './types/schema';

type Props = {
	nextStep: (fieldsToValidate: EventFormSchemaKey[]) => Promise<void>;
};

export const Step1: React.FunctionComponent<Props> = ({ nextStep }) => {
	const {
		register,
		formState: { errors },
	} = useFormContext<EventFormSchemaType>();

	return (
		<>
			<div className="form-group">
				<label htmlFor="organizerName">Your name *</label>
				<input type="text" id="organizerName" {...register('organizerName', { required: true })} aria-required="true" />
				{errors.organizerName && <span>{errors.organizerName.message}</span>}
			</div>
			<div className="form-group">
				<label htmlFor="organizerEmail">Email *</label>
				<input type="text" id="organizerEmail" {...register('organizerEmail', { required: true })} aria-required="true" />
				{errors.organizerEmail && <span>{errors.organizerEmail.message}</span>}
			</div>
			<button onClick={() => nextStep(['organizerName', 'organizerEmail'])}>Next</button>
		</>
	);
};
