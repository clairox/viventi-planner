import React from 'react';
import { useFormContext } from 'react-hook-form';
import { EventFormSchemaKey, EventFormSchemaType } from './types/schema';
import '../../styles/Form.scss';

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
				<label className={`form-label ${Boolean(errors.organizerName) && 'error'}`} htmlFor="organizerName">
					Your name *
				</label>
				<input
					type="text"
					className={`text-input ${Boolean(errors.organizerName) && 'invalid'}`}
					id="organizerName"
					{...register('organizerName', { required: true })}
					aria-required="true"
					autoFocus
				/>
				{errors.organizerName && <span className="error error-message">{errors.organizerName.message}</span>}
			</div>
			<div className="form-group">
				<label className={`form-label ${Boolean(errors.organizerEmail) && 'error'}`} htmlFor="organizerEmail">
					Email *
				</label>
				<input
					type="text"
					className={`text-input ${Boolean(errors.organizerEmail) && 'invalid'}`}
					id="organizerEmail"
					{...register('organizerEmail', { required: true })}
					aria-required="true"
				/>
				{errors.organizerEmail && <span className="error error-message">{errors.organizerEmail.message}</span>}
			</div>
			<div className="form-buttons">
				<button className="button" onClick={() => nextStep(['organizerName', 'organizerEmail'])}>
					Next
				</button>
			</div>
		</>
	);
};
