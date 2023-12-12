import { zodResolver } from '@hookform/resolvers/zod';
import { ReactElement, useEffect, useState } from 'react';
import { useForm, SubmitHandler, FormProvider } from 'react-hook-form';
import { EventFormSchema } from './utils/schema';
import { EventFormSchemaKey, EventFormSchemaType } from './types/schema';
import { Step3 } from './Step3';
import { Step2 } from './Step2';
import { Step1 } from './Step1';
import { createEvent } from '../../services/eventApi';
import { useNavigate } from 'react-router-dom';
import '../../styles/Form.scss';
import { sanitizeFormData } from '../../utils/form';

// TODO add input icons
export const EventForm = () => {
	const formMethods = useForm<EventFormSchemaType>({
		resolver: zodResolver(EventFormSchema),
		defaultValues: {
			organizerName: '',
			organizerEmail: '',
			eventName: '',
			date: new Date(),
			time: new Date(),
			eventFormat: 'virtual',
			location: '',
			description: '',
			maxCapacity: 0,
		},
	});

	const navigate = useNavigate();

	useEffect(() => {
		if (formMethods.watch('eventFormat') === 'virtual') formMethods.setValue('location', '');
	}, [formMethods, formMethods.formState]);

	const onSubmit: SubmitHandler<EventFormData> = async (data): Promise<void> => {
		const { date, time } = sanitizeFormData(data);

		const { event_id } = await createEvent({
			event_name: data.eventName,
			date: date,
			time: time,
			event_format: data.eventFormat === 'inPerson' ? 'in-person' : 'virtual',
			location_name: data.location,
			location_address: data.location,
			location_city: data.location,
			location_state: data.location,
			location_country: data.location,
			location_zip: '10001',
			organizer_name: data.organizerName,
			organizer_email: data.organizerEmail,
			event_max_capacity: data.maxCapacity,
			description: data.description,
		});

		if (event_id) {
			navigate(
				{ pathname: '/event-created', search: '?status=success&message=Form submitted successfully' },
				{ state: { status: 'success' } }
			);
		}
	};

	const [currentStep, setCurrentStep] = useState<number>(1);

	const validateFields = async (fieldsToValidate: EventFormSchemaKey[]): Promise<boolean> => {
		return (await formMethods.trigger(fieldsToValidate)) === true ? true : false;
	};

	const nextStep = async (fieldsToValidate: EventFormSchemaKey[]): Promise<void> => {
		const areFieldsValid = await validateFields(fieldsToValidate);

		if (areFieldsValid) {
			formMethods.clearErrors();
			setCurrentStep(prevStep => prevStep + 1);
		}
	};

	const prevStep = (): void => setCurrentStep(prevStep => prevStep - 1);

	const renderFormStep = (): ReactElement => {
		switch (currentStep) {
			case 1:
				return <Step1 nextStep={nextStep} />;
			case 2:
				return <Step2 prevStep={prevStep} nextStep={nextStep} />;
			case 3:
				return <Step3 prevStep={prevStep} />;
			default:
				return <></>;
		}
	};

	// TODO display form progress
	return (
		<FormProvider {...formMethods}>
			<form className="form" onSubmit={formMethods.handleSubmit(onSubmit)}>
				<h1 className="step-heading">Step {currentStep} of 3</h1>
				{renderFormStep()}
			</form>
		</FormProvider>
	);
};
