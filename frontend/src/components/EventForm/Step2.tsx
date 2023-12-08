import React from 'react';
import { useFormContext, Controller } from 'react-hook-form';
import { EventFormSchemaKey, EventFormSchemaType } from './types/schema';
import DatePicker from 'react-datepicker';
import '../../styles/Form.scss';
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
		setValue,
		formState: { errors },
	} = useFormContext<EventFormSchemaType>();

	return (
		<>
			<div className="form-group">
				<label className={`form-label ${Boolean(errors.eventName) && 'error'}`} htmlFor="eventName">
					Event name *
				</label>
				<input
					className={`text-input ${Boolean(errors.eventName) && 'invalid'}`}
					type="text"
					id="eventName"
					{...register('eventName', { required: true })}
					aria-required="true"
					autoFocus
				/>
				{errors.eventName && <span className="error error-message">{errors.eventName.message}</span>}
			</div>
			<div className="form-row">
				<div className="form-group">
					<label className={`form-label ${Boolean(errors.date) && 'error'}`} htmlFor="date">
						Date *
					</label>
					<Controller
						control={control}
						name="date"
						render={({ field: { onChange, onBlur, value } }) => (
							<DatePicker
								className={`text-input ${Boolean(errors.date) && 'invalid'}`}
								id="date"
								selected={value}
								onChange={onChange}
								onBlur={onBlur}
								autoComplete="off"
								minDate={new Date()}
							/>
						)}
					/>
					{errors.date && <span className="error error-message">{errors.date.message}</span>}
				</div>
				<div className="form-group">
					<label className={`form-label ${Boolean(errors.time) && 'error'}`} htmlFor="time">
						Time *
					</label>
					<Controller
						control={control}
						name="time"
						render={({ field: { onChange, onBlur, value } }) => (
							<DatePicker
								className={`text-input ${Boolean(errors.time) && 'invalid'}`}
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
					{errors.time && <span className="error error-message">{errors.time.message}</span>}
				</div>
			</div>
			<div className="form-group">
				<fieldset className="form-group form-row">
					<legend className={`form-label ${Boolean(errors.eventFormat) && 'error'}`}>
						Select a format for your event *
					</legend>
					<div className="radio-button-wrapper" onClick={() => setValue('eventFormat', 'virtual')}>
						<label htmlFor="virtualFormat">
							<input type="radio" id="virtualFormat" {...register('eventFormat')} value="virtual" />
							Virtual
						</label>
					</div>
					<div className="radio-button-wrapper" onClick={() => setValue('eventFormat', 'inPerson')}>
						<label htmlFor="inPersonFormat">
							<input type="radio" id="inPersonFormat" {...register('eventFormat')} value="inPerson" />
							In person
						</label>
					</div>
				</fieldset>
			</div>
			{watch('eventFormat') === 'inPerson' ? (
				<div className="form-group">
					{/* TODO add google maps search API thing */}
					<label className={`form-label ${Boolean(errors.location) && 'error'}`} htmlFor="location">
						Location *
					</label>
					<input
						type="text"
						className={`text-input ${Boolean(errors.location) && 'invalid'}`}
						id="location"
						{...register('location', { required: watch('eventFormat') === 'inPerson' })}
						aria-required={watch('eventFormat') === 'inPerson'}
					/>
					{errors.location && <span className="error error-message">{errors.location.message}</span>}
				</div>
			) : (
				<></>
			)}
			<div className="form-buttons">
				<button className="button" onClick={prevStep}>
					Back
				</button>
				<button
					className="button"
					onClick={() => nextStep(['eventName', 'date', 'time', 'eventFormat', 'location'])}
				>
					Next
				</button>
			</div>
		</>
	);
};
