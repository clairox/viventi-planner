import { Helmet } from 'react-helmet';
import { useLocation, useParams } from 'react-router-dom';
import '../styles/LinksPage.scss';

export const LinksPage = () => {
	const { eventSlug } = useParams();
	const { token } = useLocation().state;

	return (
		<section className="verified-section">
			<Helmet>
				<title>Verification Successful</title>
				<meta name="description" content="Links related to your verified event." />
			</Helmet>
			<div className="verified-details">
				<h1 className="verified-heading">Event Verified Successfully!</h1>
				<p>
					Congratulations! Your event has been successfully verified. Thank you for taking this step to ensure the accuracy and legitimacy of your event on Planner. Your event is now live and visible
					to potential attendees.
				</p>
				<div className="links-wrapper" aria-labelledby="links-heading">
					<p id="links-heading" className="links-heading">
						You can access your event details using the following links:
					</p>
					<div className="link-wrapper">
						<label htmlFor="public-link">Public shareable link:</label>
						<input id="public-link" className="link" type="text" value={`https://vvn.ti/event/${eventSlug}`} disabled />
					</div>
					<div className="link-wrapper">
						<label htmlFor="private-link">Private link for event management:</label>
						<input id="private-link" className="link" type="text" value={`https://vvn.ti/event/${eventSlug}?token=${token}`} disabled />
					</div>
				</div>
				<p>
					If you have any questions or need further assistance, feel free to contact our support team at support@planner.com. We're here to help you make your event planning experience smooth and
					enjoyable.
				</p>
				<p>Thank you for choosing Planner for your event needs!</p>
			</div>
		</section>
	);
};
