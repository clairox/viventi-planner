import { useLocation, useParams } from 'react-router-dom';

export const LinksPage = () => {
	const { eventSlug } = useParams();
	const { token } = useLocation().state;

	return (
		<section className="verified-section">
			<div>
				<h5>Event Verified Successfully!</h5>
				<p>
					Congratulations! Your event has been successfully verified. Thank you for taking this step to ensure the accuracy and legitimacy of your event on Planner. Your event is now live and visible
					to potential attendees.
				</p>
				<div className="links-section">
					<p className="links-text">You can access your event details using the following links:</p>
					<div>
						<label>Public shareable link:</label>
						<input className="link" type="text" value={`https://vvn.ti/event/${eventSlug}`} disabled />
					</div>
					<div>
						<label>Private link for event management:</label>
						<input className="link" type="text" value={`https://vvn.ti/event/${eventSlug}?token=${token}`} disabled />
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
