import React from 'react';
import { useFormContext } from 'react-hook-form';
import { EventFormSchemaType } from './types/schema';
import '../../styles/Form.scss';

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
				<label className={`form-label ${Boolean(errors.description) && 'error'}`} htmlFor="description">
					Tell us a little about your event *
				</label>
				<textarea
					className={`${Boolean(errors.description) && 'invalid'}`}
					id="description"
					{...register('description', { required: true })}
					aria-required="true"
					autoFocus
				/>
				{errors.description && <span className="error error-message">{errors.description.message}</span>}
			</div>
			<div className="form-group">
				<div className="form-inline">
					<label className={`form-label ${Boolean(errors.maxCapacity) && 'error'}`} htmlFor="maxCapacity">
						Max number of attendees *
					</label>
					<input
						type="text"
						className={`text-input small ${Boolean(errors.maxCapacity) && 'invalid'}`}
						id="maxCapacity"
						{...register('maxCapacity', { required: true })}
						aria-required="true"
					/>
				</div>
				{errors.maxCapacity && <span className="error error-message">{errors.maxCapacity.message}</span>}
			</div>
			<div className="form-buttons">
				<button className="button" onClick={prevStep}>
					Back
				</button>
				<button className="button submit" type="submit">
					Finish
				</button>
			</div>
		</>
	);
};
