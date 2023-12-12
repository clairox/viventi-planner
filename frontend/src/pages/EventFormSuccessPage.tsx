import { Navigate, useLocation } from 'react-router-dom';
import '../styles/EventFormSuccessPage.scss';

export const EventFormSuccessPage = () => {
	const location = useLocation();

	if (location.state?.status === 'success') {
		return (
			<section className="event-form-success">
				<div className="content">
					<h1 className="heading">You're almost done!</h1>
					<p>
						We've sent a verification link to your email. Please check your inbox and click the link within
						the next 7 days to complete the verification process. If you don't verify your event within this
						time frame, it will be automatically removed. Thank you for choosing our platform for your event
						planning needs!
					</p>
				</div>
			</section>
		);
	} else {
		return <Navigate to={{ pathname: '/' }} />;
	}
};
