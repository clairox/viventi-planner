import { Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { SpecialLayout } from './layouts/SpecialLayout';
import { HomePage } from './pages/HomePage';
import { VerificationRedirect } from './components/VerificationRedirect';
import { LinksPage } from './pages/LinksPage';
import './App.scss';

function App() {
	return (
		<Routes>
			<Route element={<MainLayout />}>
				<Route index element={<HomePage />} />
				<Route path="/event/activate/:token" element={<VerificationRedirect />} />
			</Route>
			<Route element={<SpecialLayout />}>
				<Route path="/event/:eventSlug/links" element={<LinksPage />} />
				<Route path="/error" element={<LinksPage />} />
			</Route>
		</Routes>
	);
}

export default App;
