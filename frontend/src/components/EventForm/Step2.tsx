import React from 'react';
import { useFormContext, Controller } from 'react-hook-form';
import { EventFormSchemaKey, EventFormSchemaType } from './types/schema';
import DatePicker from 'react-datepicker';

import 'react-datepicker/dist/react-datepicker.css';

type Props = {
	prevStep: () => void;
	nextStep: (fieldsToValidate: EventFormSchemaKey[]) => Promise<void>;
};

export const Step2: React.FunctionComponent<Props> = ({ prevStep, nextStep }) => {
	const {
		control,
		register,
		watch,
		formState: { errors },
	} = useFormContext<EventFormSchemaType>();

	return (
		<>
			<div className="form-group">
				<label htmlFor="eventName">Event name *</label>
				<input type="text" id="eventName" {...register('eventName', { required: true })} aria-required="true" />
				{errors.eventName && <span>{errors.eventName.message}</span>}
			</div>
			<div className="form-group">
				<label htmlFor="date">Date *</label>
				<Controller
					control={control}
					name="date"
					render={({ field: { onChange, onBlur, value } }) => (
						<DatePicker
							id="date"
							selected={value}
							onChange={onChange}
							onBlur={onBlur}
							autoComplete="off"
							minDate={new Date()}
						/>
					)}
				/>
				{errors.date && <span>{errors.date.message}</span>}
			</div>
			<div className="form-group">
				<label htmlFor="time">Time *</label>
				<Controller
					control={control}
					name="time"
					render={({ field: { onChange, onBlur, value } }) => (
						<DatePicker
							id="time"
							selected={value}
							onChange={onChange}
							onBlur={onBlur}
							autoComplete="off"
							minDate={new Date()}
							showTimeSelect
							showTimeSelectOnly
							timeIntervals={15}
							dateFormat="h:mm aa"
							filterTime={time => {
								const selectedDate = new Date(watch('date')?.setHours(0, 0, 0, 0));
								const currentDate = new Date(new Date().setHours(0, 0, 0, 0));
								if (selectedDate && selectedDate.getTime() == currentDate.getTime()) {
									return new Date().getTime() < new Date(time).getTime();
								}

								return true;
							}}
						/>
					)}
				/>
				{errors.time && <span>{errors.time.message}</span>}
			</div>
			<div className="form-group">
				<fieldset>
					<legend>Select a format for your event *</legend>
					<label htmlFor="virtualFormat">
						<input type="radio" id="virtualFormat" {...register('eventFormat')} value="virtual" />
						Virtual
					</label>
					<label htmlFor="inPersonFormat">
						<input type="radio" id="inPersonFormat" {...register('eventFormat')} value="inPerson" />
						In person
					</label>
				</fieldset>
			</div>
			{watch('eventFormat') === 'inPerson' ? (
				<div className="form-group">
					{/* TODO add google maps search API thing */}
					<label htmlFor="location">Location *</label>
					<input
						type="text"
						id="location"
						{...register('location', { required: watch('eventFormat') === 'inPerson' })}
						aria-required={watch('eventFormat') === 'inPerson'}
					/>
					{errors.location && <span>{errors.location.message}</span>}
				</div>
			) : (
				<></>
			)}
			<button onClick={prevStep}>Back</button>
			<button onClick={() => nextStep(['eventName', 'date', 'time', 'eventFormat', 'location'])}>Next</button>
		</>
	);
};
