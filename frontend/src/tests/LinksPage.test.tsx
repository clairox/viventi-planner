import { render } from '@testing-library/react';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import { LinksPage } from '../pages/LinksPage';

jest.mock('../styles/LinksPage.scss', () => ({}));

jest.mock('react-router-dom', () => ({
	...jest.requireActual('react-router-dom'),
	useParams: () => ({ eventSlug: 'mockSlug' }),
	useLocation: () => ({ state: { token: 'mockToken' } }),
}));

test('link inputs contain valid links', () => {
	const routes = [{ path: '/event/:eventSlug/links', element: <LinksPage /> }];

	const router = createMemoryRouter(routes, {
		initialEntries: ['/event/mockSlug/links'],
		initialIndex: 1,
	});

	const { getByLabelText } = render(<RouterProvider router={router} />);

	const publicLinkInput = getByLabelText('Public shareable link:') as HTMLInputElement;
	const privateLinkInput = getByLabelText('Private link for event management:') as HTMLInputElement;

	expect(publicLinkInput.value).toBe('https://vvn.ti/event/mockSlug');
	expect(privateLinkInput.value).toBe('https://vvn.ti/event/mockSlug?token=mockToken');
});
