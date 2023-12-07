import { z } from 'zod';
import { EventFormSchema } from '../utils/schema';

export type EventFormSchemaType = z.infer<typeof EventFormSchema>;
export type EventFormSchemaKey = keyof EventFormSchemaType;
