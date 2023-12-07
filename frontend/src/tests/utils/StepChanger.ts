import { UserEvent } from '@testing-library/user-event';
import { waitFor } from '@testing-library/react';

export class StepChanger {
	user: UserEvent;
	getByLabelText: (id: string) => HTMLElement;
	getByText: (id: string) => HTMLElement;

	constructor(user: UserEvent, getByLabelText: (id: string) => HTMLElement, getByText: (id: string) => HTMLElement) {
		this.user = user;
		this.getByLabelText = getByLabelText;
		this.getByText = getByText;
	}

	async step(step: number) {
		if (step === 2) {
			await this.changeStep(this.user, this.getByLabelText, this.getByText, 2);
		} else if (step === 3) {
			await this.changeStep(this.user, this.getByLabelText, this.getByText, 2);
			await this.changeStep(this.user, this.getByLabelText, this.getByText, 3);
		}
	}

	async setStep1Values(user: UserEvent, getByLabelText: (id: string) => HTMLElement) {
		await user.type(getByLabelText('Your name *'), 'Test User');
		await user.type(getByLabelText('Email *'), 'test@test.com');
	}

	async setStep2Values(user: UserEvent, getByLabelText: (id: string) => HTMLElement) {
		await user.type(getByLabelText('Event name *'), 'Test Event');
		await user.type(getByLabelText('Date *'), '6/3/2078');
		await user.type(getByLabelText('Time *'), '1:00 AM');
	}

	async setStep3Values(user: UserEvent, getByLabelText: (id: string) => HTMLElement) {
		await user.type(getByLabelText('Tell us a little about your event *'), 'Test Description');
		await user.type(getByLabelText('Max number of attendees *'), '1');
	}

	async changeStep(user: UserEvent, getByLabelText: (id: string) => HTMLElement, getByText: (id: string) => HTMLElement, step: number) {
		if (step === 2) {
			await this.setStep1Values(user, getByLabelText);
		}

		if (step === 3) {
			await this.setStep2Values(user, getByLabelText);
		}

		if (step === 4) {
			await this.setStep3Values(user, getByLabelText);
		}

		await user.click(getByText('Next'));
		await waitFor(() => getByText(`Step ${step} of 3`));
	}
}
