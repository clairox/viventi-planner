import { Outlet } from 'react-router-dom';

export const SpecialLayout = () => {
	return (
		<div className="container special">
			<main className="main">
				<Outlet />
			</main>
		</div>
	);
};
