import { TimeZone, getTimeZones } from '@vvo/tzdb';

const getUTCOffset = (offsetInMinutes: number): string => {
	const plusOrMinus = offsetInMinutes > 0 ? '+' : offsetInMinutes === 0 ? '' : '-';
	const hours = Math.floor(Math.abs(offsetInMinutes) / 60).toString();
	const minutes = Math.abs(offsetInMinutes % 60)
		.toString()
		.padStart(2, '0');

	return plusOrMinus ? plusOrMinus + hours + ':' + minutes : '';
};

export const defaultTimeZone: TzType = {
	name: 'America/New York',
	value: 'America/New_York',
	offsetInMinutes: -300,
	utcOffset: getUTCOffset(-300),
};

export const getTimezone = (tzName: string): TzType | undefined => {
	return getAllTimezones().find(timezone => timezone.value === tzName);
};

export const getAllTimezones = (): TzType[] => {
	return getTimeZones()
		.map((tz: TimeZone) => {
			return {
				name: tz.name.replace('_', ' '),
				value: tz.name,
				offsetInMinutes: tz.currentTimeOffsetInMinutes,
				utcOffset: getUTCOffset(tz.currentTimeOffsetInMinutes),
			};
		})
		.sort((a, b) => {
			if (a.name < b.name) return -1;
			if (a.name > b.name) return 1;
			return 0;
		});
};
