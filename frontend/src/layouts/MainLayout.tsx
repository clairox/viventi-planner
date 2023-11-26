import { Outlet } from 'react-router-dom';

export const MainLayout = () => {
	return (
		<div className="container">
			<main className="content-area">
				<Outlet />
			</main>
		</div>
	);
};
